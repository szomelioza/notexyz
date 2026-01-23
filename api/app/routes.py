from flask import Blueprint

from .utils.notes import get_latest_note_content

bp = Blueprint("api", __name__)


@bp.get("/note")
def get_note():
    note_text = get_latest_note_content()
    return {"result": note_text}
