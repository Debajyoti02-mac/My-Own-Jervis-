import base64
from datetime import datetime, timedelta
from email.message import EmailMessage
from functools import lru_cache

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.tools import tool
from langgraph.types import interrupt

from settings import CREDENTIALS_FILE, TOKEN_FILE
from tools.common import is_yes

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.events",
]


def google_creds():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


@lru_cache(maxsize=None)
def _gmail():
    return build("gmail", "v1", credentials=google_creds())


@lru_cache(maxsize=None)
def _calendar():
    return build("calendar", "v3", credentials=google_creds())


@tool
def read_unread_emails(max_results: int = 5) -> str:
    """List the user's latest unread inbox emails (sender, subject, short preview)."""
    try:
        msgs = _gmail().users().messages().list(
            userId="me", q="is:unread in:inbox", maxResults=min(max_results, 10)
        ).execute().get("messages", [])
        if not msgs:
            return "No unread emails."
        lines = []
        for m in msgs:
            d = _gmail().users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From", "Subject"],
            ).execute()
            h = {x["name"]: x["value"] for x in d["payload"]["headers"]}
            lines.append(f"From: {h.get('From', '?')} | Subject: {h.get('Subject', '(none)')} | {d.get('snippet', '')[:120]}")
        return "\n".join(lines)
    except Exception as e:
        return f"Gmail error: {e}"


@tool
def get_events(days: int = 1) -> str:
    """List the user's calendar events from now until N days ahead (default 1 day)."""
    try:
        now = datetime.now().astimezone()
        events = _calendar().events().list(
            calendarId="primary", timeMin=now.isoformat(),
            timeMax=(now + timedelta(days=days)).isoformat(),
            singleEvents=True, orderBy="startTime", maxResults=10,
        ).execute().get("items", [])
        if not events:
            return "No upcoming events."
        return "\n".join(
            f"{e['start'].get('dateTime', e['start'].get('date'))}: {e.get('summary', '(no title)')}"
            for e in events
        )
    except Exception as e:
        return f"Calendar error: {e}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email from the user's Gmail. Always asks the user to confirm the exact draft first."""
    answer = interrupt(f"SEND EMAIL?\nTo: {to}\nSubject: {subject}\n\n{body}\n\nType yes to send:")
    if not is_yes(answer):
        return "Cancelled. Nothing was sent."
    try:
        msg = EmailMessage()
        msg["To"], msg["Subject"] = to, subject
        msg.set_content(body)
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        _gmail().users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to}."
    except Exception as e:
        return f"Send failed: {e}"


@tool
def create_event(title: str, start: str, duration_minutes: int = 60) -> str:
    """Create a calendar event. start is ISO format like 2026-10-25T15:00. Always asks the user to confirm first."""
    answer = interrupt(f"CREATE EVENT?\n{title}\nStart: {start}\nDuration: {duration_minutes} min\n\nType yes to create:")
    if not is_yes(answer):
        return "Cancelled. No event created."
    try:
        begin = datetime.fromisoformat(start)
        if begin.tzinfo is None:
            begin = begin.astimezone()
        end = begin + timedelta(minutes=duration_minutes)
        _calendar().events().insert(calendarId="primary", body={
            "summary": title,
            "start": {"dateTime": begin.isoformat()},
            "end": {"dateTime": end.isoformat()},
        }).execute()
        return f"Event created: {title}"
    except Exception as e:
        return f"Event failed: {e}"


GOOGLE_TOOLS = [read_unread_emails, get_events, send_email, create_event]