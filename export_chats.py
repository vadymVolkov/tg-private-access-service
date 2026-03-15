import asyncio
import csv
from telethon.tl.types import Channel
from src.config import get_config
from src.telegram_client import create_client, session_exists

CSV_FILE = "chats.csv"


def get_chat_type(entity) -> str:
    if isinstance(entity, Channel):
        return "channel" if entity.broadcast else "supergroup"
    return "group"


async def main():
    config = get_config()

    if not session_exists(config["session_name"]):
        print("Session not found. Please run authorize.py first.")
        return

    client = create_client(config["api_id"], config["api_hash"], config["session_name"])
    await client.connect()

    if not await client.is_user_authorized():
        print("Session is invalid or expired. Please run authorize.py again.")
        await client.disconnect()
        return

    print("Loading dialogs...")
    dialogs = await client.get_dialogs()

    chats = []
    for dialog in dialogs:
        entity = dialog.entity
        if not isinstance(entity, (Channel,)) and not hasattr(entity, "title"):
            continue
        # Skip private user chats
        from telethon.tl.types import User
        if isinstance(entity, User):
            continue
        chats.append({
            "id": entity.id,
            "title": dialog.name or "",
            "type": get_chat_type(entity),
            "username": getattr(entity, "username", "") or "",
            "members_count": getattr(entity, "participants_count", "") or "",
        })

    if not chats:
        print("No channels or groups found.")
        await client.disconnect()
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "type", "username", "members_count"])
        writer.writeheader()
        writer.writerows(chats)

    print(f"Saved {len(chats)} chats to {CSV_FILE}")
    for i, chat in enumerate(chats, 1):
        username = f"@{chat['username']}" if chat["username"] else "-"
        print(f"{i}. {chat['title']} | {chat['type']} | {username} | id: {chat['id']}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
