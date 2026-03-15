import os
from telethon import TelegramClient


def create_client(api_id: int, api_hash: str, session_name: str) -> TelegramClient:
    sessions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    session_path = os.path.join(sessions_dir, session_name)
    return TelegramClient(session_path, api_id, api_hash)


def session_exists(session_name: str) -> bool:
    sessions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sessions")
    return os.path.exists(os.path.join(sessions_dir, f"{session_name}.session"))
