from flask import Blueprint

from .utils.notes import today_note_exists

bp = Blueprint("api", __name__)


@bp.get("/note")
def get_note():
    if today_note_exists():
        return {"result": "Exists!"}
    return {"result": "missing"}
