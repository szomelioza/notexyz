import base64
import json
import socket
from io import BytesIO
from urllib.parse import quote

import markdown
import requests
import websocket
from PIL import Image

from .settings import HEADLESS_ADDRESS


def generate_image_headless(text):
    """
    Generate image using headless browser.
    """
    html_content = get_html_content(text)
    target_url = get_json_target_url()
    targets = requests.get(target_url).json()
    ws_url = targets[0]["webSocketDebuggerUrl"]

    try:
        ws = websocket.create_connection(ws_url)
        ws.settimeout(3)

        ws_send(ws=ws, method="Page.enable", msg_id=1)

        encoded_html = quote(html_content)
        ws_send(
            ws=ws,
            method="Page.navigate",
            msg_id=2,
            params={"url": f"data:text/html,{encoded_html}"}
        )
        while True:
            try:
                resp = json.loads(ws.recv())
                if resp.get("method") == "Page.loadEventFired":
                    break
            except websocket.WebSocketTimeoutException:
                break

        ws_send(
            ws,
            "Page.captureScreenshot",
            msg_id=3,
            params={"format": "png"}
        )
        while True:
            try:
                resp = json.loads(ws.recv())
                if resp.get("id") == 3:
                    screenshot_data = resp["result"]["data"]
                    break
            except websocket.WebSocketTimeoutException:
                raise RuntimeError(
                    "Headless browser failed to return screenshot"
                )
    finally:
        ws.close()
    screenshot_bytes = base64.b64decode(screenshot_data)
    return Image.open(BytesIO(screenshot_bytes))


def get_json_target_url():
    """
    Get URL to fetch WebSocket Address using IP instead of hostname.
    """
    domain, port = HEADLESS_ADDRESS.split(":")
    ip = socket.gethostbyname(domain)
    return f"http://{ip}:{port}/json"


def ws_send(ws, method, msg_id, params=None):
    """
    Send command to headless browser via websocket and return response.
    """
    payload = {
        "id": msg_id,
        "method": method,
    }
    if params:
        payload["params"] = params
    ws.send(json.dumps(payload))


def get_html_content(text):
    """
    Convert markdown content to HTML.
    """
    markdown_content = markdown.markdown(text).strip()
    html_content = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset='utf-8'>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
          href="https://fonts.googleapis.com/css2?family=Ubuntu&display=swap"
          rel="stylesheet"
        >
        <style>
            body {{
                font-family: 'Ubuntu', sans-serif;
                margin-top: 50px;
                margin-left: 15px;
            }}
            strong {{ font-weight: bold; }}
            em {{ font-style: italic; }}
            u {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        {markdown_content}
    </body>
    </html>
    """.strip()
    return html_content
