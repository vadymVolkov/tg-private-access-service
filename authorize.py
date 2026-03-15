import asyncio
from src.config import get_config
from src.telegram_client import create_client, session_exists


async def main():
    config = get_config()

    if session_exists(config["session_name"]):
        print(f"Session '{config['session_name']}' already exists. You are already authorized.")
        return

    client = create_client(config["api_id"], config["api_hash"], config["session_name"])

    await client.start()

    me = await client.get_me()
    print(f"Successfully authorized as: {me.first_name} (@{me.username})")
    print(f"Session saved as: sessions/{config['session_name']}.session")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
