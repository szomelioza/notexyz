import io

from flask import Blueprint, Response

from .utils.images import get_image
from .utils.notes import get_latest_note

bp = Blueprint("api", __name__)


@bp.get("/note")
def get_note():
    note_text = get_latest_note()

    image = get_image(note_text)
    buffer = io.BytesIO()
    image.save(buffer, format="BMP")
    buffer.seek(0)

    return Response(
        buffer.getvalue(),
        mimetype="image/bmp",
        headers={"Content-Disposition": "inline"}
    )
