import hashlib
from datetime import datetime

from PIL import Image, ImageDraw

from .basic_renderer import generate_image_basic
from .headless_renderer import generate_image_headless
from .settings import (FONT_BOLD, FONT_REGULAR, HEADLESS_ADDRESS, IMAGES_DIR,
                       IMG_WIDTH)


def get_image(text, recreate=False, basic=False):
    """
    Check if image already exists and return it.
    If not create it and return it.
    """
    image_path = get_image_path(text)
    if not recreate:
        if image_path.is_file():
            image = Image.open(image_path)
    else:
        if HEADLESS_ADDRESS and not basic:
            try:
                image = generate_image_headless(text)
            except Exception as e:
                print(f"Headless rendering failed: {e}")
                image = generate_image_basic(text)
        else:
            image = generate_image_basic(text)
        add_logo(image)
        rotate_image_file(image, image_path)

    image = add_sync_time(image)
    return image


def add_sync_time(image):
    """
    Add sync time to the image.
    """
    draw = ImageDraw.Draw(image)
    text = f"sync: {datetime.now().strftime('%H:%M:%S')}"

    bbox = draw.textbbox((0, 0), text, font=FONT_REGULAR)
    text_width = bbox[2] - bbox[0]
    x = IMG_WIDTH - text_width - 5
    y = 5

    draw.text((x, y), text, fill=0, font=FONT_REGULAR)
    return image


def add_logo(image):
    """
    Add logo (text + horizontal line) to an image.
    """
    draw = ImageDraw.Draw(image)
    text = "notexyz"
    x, y = 5, 5
    draw.text((x, y), text, fill=0, font=FONT_BOLD)

    x0, y0 = 5, 25
    x1, y1 = IMG_WIDTH - 5, 25
    draw.line((x0, y0, x1, y1), fill=0)
    return image


def get_image_path(text):
    """
    Create an image path based on SHA256 hash of the text.
    """
    image_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    image_path = IMAGES_DIR / f"{image_hash}.bmp"
    return image_path


def rotate_image_file(image, path):
    """
    Delete old image and save new one.
    """
    for bmp_file in IMAGES_DIR.glob("*.bmp"):
        bmp_file.unlink()
    image.save(path, format="BMP")
