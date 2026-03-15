"""
Usage:
    python chat_info.py <chat_id>
    python chat_info.py <index>   (index from chats.csv, starting at 1)
"""
import asyncio
import csv
import sys
from telethon.tl.types import Channel, Chat
from src.config import get_config
from src.telegram_client import create_client, session_exists

CSV_FILE = "chats.csv"


def resolve_chat_id(arg: str) -> int:
    """Return chat ID from a direct ID or a 1-based index from CSV."""
    try:
        value = int(arg)
    except ValueError:
        print(f"Error: '{arg}' is not a valid number.")
        sys.exit(1)

    # Try to treat as index first if CSV exists and value looks like a small number
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if 1 <= value <= len(rows):
            # Ambiguous — prefer index if value is within CSV range
            chat_id = int(rows[value - 1]["id"])
            print(f"Resolved index {value} → id: {chat_id} ({rows[value - 1]['title']})")
            return chat_id
    except FileNotFoundError:
        pass

    return value


async def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_info.py <chat_id_or_index>")
        print("  chat_id  — Telegram chat ID")
        print("  index    — row number from chats.csv (run export_chats.py first)")
        sys.exit(1)

    config = get_config()

    if not session_exists(config["session_name"]):
        print("Session not found. Please run authorize.py first.")
        return

    chat_id = resolve_chat_id(sys.argv[1])

    client = create_client(config["api_id"], config["api_hash"], config["session_name"])
    await client.connect()

    if not await client.is_user_authorized():
        print("Session is invalid or expired. Please run authorize.py again.")
        await client.disconnect()
        return

    try:
        entity = await client.get_entity(chat_id)
    except Exception as e:
        print(f"Could not find chat with id {chat_id}: {e}")
        await client.disconnect()
        return

    print("\n--- Chat Info ---")
    print(f"Title       : {getattr(entity, 'title', getattr(entity, 'first_name', ''))}")
    print(f"ID          : {entity.id}")

    if isinstance(entity, Channel):
        chat_type = "channel" if entity.broadcast else "supergroup"
    elif isinstance(entity, Chat):
        chat_type = "group"
    else:
        chat_type = "user"

    print(f"Type        : {chat_type}")
    username = getattr(entity, "username", None)
    print(f"Username    : @{username}" if username else "Username    : -")

    if hasattr(entity, "participants_count") and entity.participants_count:
        print(f"Members     : {entity.participants_count}")

    if isinstance(entity, Channel):
        print(f"Verified    : {getattr(entity, 'verified', False)}")
        print(f"Scam        : {getattr(entity, 'scam', False)}")
        if entity.username:
            print(f"Link        : https://t.me/{entity.username}")

    # Fetch full info for description
    try:
        if isinstance(entity, Channel):
            from telethon.tl.functions.channels import GetFullChannelRequest
            full = await client(GetFullChannelRequest(entity))
            about = full.full_chat.about
        elif isinstance(entity, Chat):
            from telethon.tl.functions.messages import GetFullChatRequest
            full = await client(GetFullChatRequest(entity.id))
            about = full.full_chat.about
        else:
            about = None

        if about:
            print(f"Description : {about}")
    except Exception:
        pass

    print("-----------------\n")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
