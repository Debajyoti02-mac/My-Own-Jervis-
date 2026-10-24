from datetime import datetime 
from langchain_core.tools import tool 
from langgraph.types import interrupt 

from settings import NOTES_FILE
from tools.common import is_yes


@tool
def get_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


@tool
def save_note(text: str) -> str:
    """Save a note for the user."""
    with open(NOTES_FILE, "a") as f:
        f.write(text + "\n")
    return "Note saved successfully."


@tool
def read_notes() -> str:
    """Read all of the user's saved notes."""
    try:
        return NOTES_FILE.read_text() or "No notes yet."
    except FileNotFoundError:
        return "No notes yet."


@tool
def delete_notes() -> str:
    """Delete all of the user's saved notes. Always asks the user to confirm first."""
    answer = interrupt("Delete ALL notes? (yes/no)")
    if not is_yes(answer):
        return "Cancelled. Nothing was deleted."
    NOTES_FILE.write_text("")
    return "All notes deleted."


NOTES_TOOLS = [get_time, save_note, read_notes, delete_notes]