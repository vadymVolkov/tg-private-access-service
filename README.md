# Telegram Account Service

A minimal Python console service that interacts with a Telegram user account via the Telegram API using [Telethon](https://github.com/LonamiWebs/Telethon).

## Requirements

- Python 3.11+

## Installation

**Clone the repository:**

```bash
git clone <repository-url>
cd tg-private-access-service
```

**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the environment:**

- Linux/macOS: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Install dependencies:**

```bash
pip install -r requirements.txt
```

## Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Then fill in the values in `.env`:

```
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
TG_SESSION_NAME=my_telegram_session
```

## Getting Telegram API Credentials

You need a Telegram API ID and API Hash to use this service.

1. Log in at [https://my.telegram.org](https://my.telegram.org) with your Telegram phone number.
2. Go to **API development tools**.
3. Create a new application (name and platform do not matter for personal use).
4. Copy the **App api_id** and **App api_hash** into your `.env` file.

## First Time Authorization

Run the authorization script:

```bash
python authorize.py
```

The script will prompt for:
- Your phone number (in international format, e.g. `+1234567890`)
- The login code sent to your Telegram app
- Your 2FA password (if two-factor authentication is enabled)

After successful login, your Telegram session will be saved locally in the `sessions/` directory.

You only need to run this once. The session persists between runs.

## Getting Chats

Once authorized, print your first 10 chats:

```bash
python get_chats.py
```

Example output:

```
First 10 chats:

1. John Doe | user | id: 12345678
2. Crypto Group | group | id: 98765432
3. News Channel | channel | id: 11223344
```

## Security Note

- **Never commit your `.env` file** — it contains your API credentials.
- **Never commit session files** — they provide full access to your Telegram account.
- Both `.env` and `sessions/` are already excluded via `.gitignore`.
- Keep your session files local and secure.
