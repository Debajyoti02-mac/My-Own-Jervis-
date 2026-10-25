import subprocess 
from urllib.parse import quote_plus , urlparse 

from langchain_core.tools import tool 
from langgraph.types import interrupt 

from settings import BROWSER 
from tools.common import is_yes 

def _open(url:str)->str:
    result = subprocess.run(["open", "-a", BROWSER, url], capture_output=True, text=True)
    
    if result.returncode!=0:
        return f"Could not open {BROWSER} : {result.stderr.strip()}"
    return "Opened"

@tool
def youtube_search(query: str) -> str:
    """Open YouTube search results for a query in the user's browser."""
    return _open("https://www.youtube.com/results?search_query=" + quote_plus(query))

@tool
def open_website(url: str) -> str:
    """Open a website in the user's browser. Always asks the user to confirm the address first."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parts = urlparse(url)
    if not parts.netloc:
        return "That is not a valid web address."
    answer = interrupt(f"OPEN WEBSITE?\n{url}\n\nType yes to open:")
    if not is_yes(answer):
        return "Cancelled. Nothing was opened."
    return _open(url)

BROWSER_TOOLS = [youtube_search, open_website]