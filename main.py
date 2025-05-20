"""Main module for the AI Stick Notes MCP server."""
import os
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AI Stick Notes")

# Caminho absoluto para o diretório do script atual (raiz do projeto)
project_root = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para o arquivo
NOTES_FILE = os.path.join(project_root, "notes.txt")


def ensure_file():
    """Ensure the notes file exists; create it if it does not."""
    # Test write permissions
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write("")


@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky notes file.

    Args:
        message (str): The message to add to the notes file.

    Returns:
        str: Confirmation message indicating that the note was saved.
    """
    ensure_file()
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    return "Note saved!"


@mcp.tool()
def get_notes() -> str:
    """
    Read and return all notes from the sticky notes file.

    Returns:
        str: All notes as a single string separated by line breaks.
        If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return content or "No notes yet."


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the sticky notes file.

    Returns:
        str: The latest note or a default message if no notes exist.
    """
    ensure_file()
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes yet."


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.

    Returns:
        str: A prompt string that includes all notes and asks for a summary.
             If no notes exist, a message will be shown indicating that.
    """
    ensure_file()
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return "There are no notes yet."
    return f"Summarize the current notes: {content}"
