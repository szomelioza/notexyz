from PIL import Image, ImageDraw

from .settings import FONT_REGULAR, IMG_HEIGHT, IMG_WIDTH


def generate_image_basic(text):
    """
    Generate image from given text.
    """
    lines = wrap_text(text, IMG_WIDTH - 20)
    image = Image.new("1", (IMG_WIDTH, IMG_HEIGHT), color=1)
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
