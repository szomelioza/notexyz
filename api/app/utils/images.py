import hashlib
import os
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Fonts
UTILS_DIR = Path(__file__).parent
STATIC_DIR = UTILS_DIR.parent / "static"
FONT_REGULAR_PATH = STATIC_DIR / "Ubuntu-Regular.ttf"
FONT_BOLD_PATH = STATIC_DIR / "Ubuntu-Bold.ttf"
FONT_SIZE = 15
FONT_REGULAR = ImageFont.truetype(str(FONT_REGULAR_PATH), FONT_SIZE)
FONT_BOLD = ImageFont.truetype(str(FONT_BOLD_PATH), FONT_SIZE)


# Images
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
    text = f"sync: {datetime.now().strftime('%H:%M:%S')}"

    bbox = draw.textbbox((0, 0), text, font=FONT_REGULAR)
    text_width = bbox[2] - bbox[0]
    x = IMG_WIDTH - text_width - 5
    y = 5

    draw.text((x, y), text, fill=0, font=FONT_REGULAR)
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
    lines = wrap_text(text, IMG_WIDTH - 20)
    image = Image.new("1", (IMG_WIDTH, IMG_HEIGHT), color=1)
    image = add_logo(image)
    draw = ImageDraw.Draw(image)
    x, y = 15, 50
    y_offset = 25
    for line in lines:
        draw.text((x, y), line, fill=0, font=FONT_REGULAR)
        y += y_offset
    return image


def wrap_text(text, max_width):
    """
    Wrap text so it fits image width.
    """
    test_img = Image.new("1", (1, 1))
    test_draw = ImageDraw.Draw(test_img)

    lines = []
    for parapgraph in text.split("\n"):
        words = parapgraph.split(" ")
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_line_bbox = test_draw.textbbox(
                (0, 0),
                test_line,
                font=FONT_REGULAR
            )
            test_line_width = test_line_bbox[2] - test_line_bbox[0]
            if test_line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

    return lines


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


def rotate_image_file(image, path):
    """
    Delete old image and save new one.
    """
    for bmp_file in IMAGES_DIR.glob("*.bmp"):
        bmp_file.unlink()
    image.save(path)
