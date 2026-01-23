import os
from datetime import datetime
from pathlib import Path

NOTES_DIR = os.getenv("NOTES_DIR", "notes")
NOTES_DIR = Path(NOTES_DIR)


def today_note_exists():
    """
    Check if a note for today exists in the NOTES_DIR.
    """
    today_str = datetime.now().strftime("%d-%m-%Y")
    file_path = NOTES_DIR / f"{today_str}.md"
    return file_path.is_file()
