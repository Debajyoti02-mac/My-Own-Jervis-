Model = "openai/gpt-oss-120b"

from pathlib import Path 
from dotenv import load_dotenv 

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

ASSISTANT_NAME = "Jarvis"
MODEL = "openai/gpt-oss-120b"
MAX_MESSAGES = 20
CREATOR = "Debajyoti"

DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


NOTES_FILE = DATA / "Note.txt"
DB_FILE = DATA / "mate_memory.db"
CHROMA_DIR = DATA / "mate_chroma"
TOKEN_FILE = DATA / "token.json"
CREDENTIALS_FILE = ROOT / "credentials.json"

WAKE_MODEL = "hey_jarvis_v0.1.onnx"
WAKE_THRESHOLD = 0.4

DEFAULT_CITY = "" 
