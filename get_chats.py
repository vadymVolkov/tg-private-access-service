import asyncio
from telethon.tl.types import User, Chat, Channel
from src.config import get_config
from src.telegram_client import create_client, session_exists


def get_chat_type(entity) -> str:
    if isinstance(entity, User):
        return "user"
    if isinstance(entity, Chat):
        return "group"
    if isinstance(entity, Channel):
        return "channel" if entity.broadcast else "supergroup"
    return "unknown"


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

    dialogs = await client.get_dialogs(limit=10)

    if not dialogs:
        print("No chats found.")
        await client.disconnect()
        return

    print(f"First {len(dialogs)} chats:\n")
    for i, dialog in enumerate(dialogs, start=1):
        entity = dialog.entity
        chat_type = get_chat_type(entity)
        title = dialog.name or "Unknown"
        chat_id = entity.id
        print(f"{i}. {title} | {chat_type} | id: {chat_id}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
