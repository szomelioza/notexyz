import os
from datetime import datetime
from pathlib import Path

NOTES_DIR = Path(os.getenv("NOTES_DIR", "notes"))


def get_latest_note_content():
    """
    Get content of the latest note.
    """
    today_note_path = NOTES_DIR / datetime.now().strftime("%d-%m-%Y.md")
    if today_note_path.is_file():
        return read_note(today_note_path)

    dates = []
    for path in list(NOTES_DIR.glob("*.md")):
        try:
            note_date = datetime.strptime(path.stem, "%d-%m-%Y")
            dates.append((note_date, path))
        except ValueError:
            pass
    latest_note_path = max(dates, key=lambda note: note[0])[1]
    return read_note(latest_note_path)


def read_note(path):
    """
    Get content of the note by given path.
    """
    return path.read_text(encoding="utf-8")
