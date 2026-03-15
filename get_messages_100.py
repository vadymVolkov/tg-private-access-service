"""
Usage:
    python get_messages_100.py <chat_id>
    python get_messages_100.py <index>   (index from chats.csv, starting at 1)
"""
import asyncio
import sys
from src.config import get_config
from src.telegram_client import create_client, session_exists
from src.messages import resolve_chat_id, fetch_and_print_messages


async def main():
    if len(sys.argv) < 2:
        print("Usage: python get_messages_100.py <chat_id_or_index>")
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

    await fetch_and_print_messages(client, chat_id, limit=100)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
