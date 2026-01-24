import hashlib
import os
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "images"))
IMG_WIDTH, IMG_HEIGHT = 400, 300


def get_image(text):
    """
    Check if image already exists and return it.
    If not create it and return it.
    """
    image_path = get_image_path(text)
    if image_path.is_file():
        image = Image.open(image_path)
    else:
        image = generate_image(text)
        rotate_image_file(image, image_path)

    image = add_sync_time(image)
    return image


def add_sync_time(image):
    """
    Add sync time to the image.
    """
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = f"sync: {datetime.now().strftime('%H:%M:%S')}"

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = IMG_WIDTH - text_width - 5
    y = 5

    draw.text((x, y), text, fill=0, font=font)
    return image


def get_image_path(text):
    """
    Create an image path based on SHA256 hash of the text.
    """
    image_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    image_path = IMAGES_DIR / f"{image_hash}.bmp"
    return image_path


def generate_image(text):
    """
    Generate image from give text.
    """
    lines = text.split("\n")
    image = Image.new("1", (IMG_WIDTH, IMG_HEIGHT), color=1)
    image = add_logo(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    x, y = 5, 25
    y_offset = 20
    for line in lines:
        draw.text((x, y), line, fill=0, font=font)
        y += y_offset
    return image


def add_logo(image):
    """
    Add logo (text + horizontal line) to an image.
    """
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = "notexyz"
    x, y = 5, 5
    draw.text((x, y), text, fill=0, font=font)

    x0, y0 = 5, 20
    x1, y1 = IMG_WIDTH - 5, 20
    draw.line((x0, y0, x1, y1), fill=0)
    return image


def rotate_image_file(image, path):
    """
    Delete old image and save new one.
    """
    for bmp_file in IMAGES_DIR.glob("*.bmp"):
        bmp_file.unlink()
    image.save(path)
