import csv
import sys
from telethon.tl.types import User

CSV_FILE = "chats.csv"


def resolve_chat_id(arg: str) -> int:
    """Return chat ID from a direct ID or a 1-based index from CSV."""
    try:
        value = int(arg)
    except ValueError:
        print(f"Error: '{arg}' is not a valid number.")
        sys.exit(1)

    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if 1 <= value <= len(rows):
            chat_id = int(rows[value - 1]["id"])
            print(f"Resolved index {value} → id: {chat_id} ({rows[value - 1]['title']})")
            return chat_id
    except FileNotFoundError:
        pass

    return value


async def fetch_and_print_messages(client, chat_id: int, limit: int):
    try:
        entity = await client.get_entity(chat_id)
    except Exception as e:
        print(f"Could not find chat with id {chat_id}: {e}")
        return

    title = getattr(entity, "title", getattr(entity, "first_name", str(chat_id)))
    print(f"\n--- Last {limit} messages from: {title} ---\n")

    messages = await client.get_messages(entity, limit=limit)

    if not messages:
        print("No messages found.")
        return

    for msg in reversed(messages):
        date = msg.date.strftime("%Y-%m-%d %H:%M")

        sender_name = "Unknown"
        if msg.sender:
            sender = msg.sender
            if isinstance(sender, User):
                parts = [sender.first_name or "", sender.last_name or ""]
                sender_name = " ".join(p for p in parts if p).strip() or f"id:{sender.id}"
            else:
                sender_name = getattr(sender, "title", f"id:{sender.id}")

        text = msg.text or "[media/service message]"
        print(f"[{date}] {sender_name}: {text}")

    print(f"\n--- End of messages ---\n")
