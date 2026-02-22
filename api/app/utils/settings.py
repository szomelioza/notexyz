import os
from pathlib import Path

from PIL import ImageFont

# Fonts
UTILS_DIR = Path(__file__).parent
STATIC_DIR = UTILS_DIR.parent / "static"
FONT_REGULAR_PATH = STATIC_DIR / "Ubuntu-Regular.ttf"
FONT_BOLD_PATH = STATIC_DIR / "Ubuntu-Bold.ttf"
FONT_SIZE = 15
FONT_REGULAR = ImageFont.truetype(str(FONT_REGULAR_PATH), FONT_SIZE)
FONT_BOLD = ImageFont.truetype(str(FONT_BOLD_PATH), FONT_SIZE)


# Images
IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "/images"))
IMG_WIDTH, IMG_HEIGHT = 400, 300

# Headless
HEADLESS_ADDRESS = os.getenv("HEADLESS_ADDRESS")
