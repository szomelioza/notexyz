import io

from flask import Blueprint, Response, request

from .utils.images import get_image
from .utils.notes import get_latest_note

bp = Blueprint("api", __name__)


@bp.get("/note")
def get_note():
    stream = request.args.get("stream", "false").lower() == "true"
    recreate = request.args.get("recreate", "false").lower() == "true"
    basic = request.args.get("basic", "false").lower() == "true"
    note_text = get_latest_note()
    image = get_image(note_text, recreate=recreate, basic=basic)

    if stream:
        image = image.convert("1")
        raw = image.tobytes()
        return Response(
            raw,
            mimetype="application/octet-stream",
        )

    buffer = io.BytesIO()
    image.save(buffer, format="BMP")
    buffer.seek(0)

    return Response(
        buffer.getvalue(),
        mimetype="image/bmp",
        headers={"Content-Disposition": "inline"}
    )
