import uuid
import chromadb
from ddgs import DDGS
from langchain_core.tools import tool

from settings import CHROMA_DIR

_chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
_facts = _chroma.get_or_create_collection("facts")


@tool
def remember_facts(fact: str) -> str:
    """Save a lasting fact about the user (name, studies, preferences, goals) for future conversations."""
    _facts.add(documents=[fact], ids=[str(uuid.uuid4())])
    return "Remembered."


@tool
def recall_facts(query: str) -> str:
    """Search saved facts about the user. Use when asked about the user or past details."""
    if _facts.count() == 0:
        return "No saved facts."
    res = _facts.query(query_texts=[query], n_results=min(3, _facts.count()))
    return "\n".join(res["documents"][0])


@tool
def web_search(query: str) -> str:
    """Search the web for current information, news, or facts Mate does not know."""
    try:
        results = DDGS().text(query, max_results=4)
    except Exception as e:
        return f"Search failed: {e}"
    if not results:
        return "No results found."
    return "\n".join(f"{r['title']}: {r['body'][:300]} ({r['href']})" for r in results)


MEMORY_WEB_TOOLS = [remember_facts, recall_facts, web_search]