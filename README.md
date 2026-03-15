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

1. Log in at [https://my.telegram.org](https://my.telegram.org) with your Telegram phone number.
2. Go to **API development tools**.
3. Create a new application (name and platform do not matter for personal use).
4. Copy the **App api_id** and **App api_hash** into your `.env` file.

## Scripts

### 1. First time authorization

Run once to authenticate your Telegram account:

```bash
python authorize.py
```

The script will prompt for:
- Your phone number (in international format, e.g. `+1234567890`)
- The login code sent to your Telegram app
- Your 2FA password (if two-factor authentication is enabled)

After successful login, the session is saved to `sessions/` and reused automatically.

---

### 2. List first 10 chats

```bash
python get_chats.py
```

Prints the first 10 dialogs (all types) with name, type, and ID.

---

### 3. Export channels and groups to CSV

```bash
python export_chats.py
```

Fetches all channels and groups the user is a member of and saves them to `chats.csv`:

```
id,title,type,username,members_count
```

Also prints the list to the terminal with index numbers. Use those indexes in the scripts below.

---

### 4. Get info about a channel or group

```bash
python chat_info.py <chat_id_or_index>
```

- `chat_id` — Telegram chat ID (e.g. `-1001234567890`)
- `index` — row number from `chats.csv` (run `export_chats.py` first)

Example:

```bash
python chat_info.py 3
python chat_info.py -1001234567890
```

Prints title, type, username, member count, description, and link.

---

### 5. Get last 20 messages from a chat

```bash
python get_messages_20.py <chat_id_or_index>
```

Example:

```bash
python get_messages_20.py 3
python get_messages_20.py -1001234567890
```

---

### 6. Get last 100 messages from a chat

```bash
python get_messages_100.py <chat_id_or_index>
```

Example:

```bash
python get_messages_100.py 3
python get_messages_100.py -1001234567890
```

---

## Typical Workflow

```bash
# 1. Authorize once
python authorize.py

# 2. Export all channels and groups to CSV (with index numbers)
python export_chats.py

# 3. View info about chat #3 from the list
python chat_info.py 3

# 4. Read last 20 messages from chat #3
python get_messages_20.py 3

# 5. Read last 100 messages from chat #3
python get_messages_100.py 3
```

---

## Project Structure

```
tg-private-access-service/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── authorize.py          # Authorize Telegram account
├── get_chats.py          # Print first 10 dialogs
├── export_chats.py       # Export channels/groups to chats.csv
├── chat_info.py          # Show info about a channel/group
├── get_messages_20.py    # Print last 20 messages
├── get_messages_100.py   # Print last 100 messages
├── sessions/             # Session files (gitignored)
└── src/
    ├── config.py         # Load and validate .env
    ├── telegram_client.py # Telethon client factory
    └── messages.py       # Shared message fetching logic
```

## Security Note

- **Never commit your `.env` file** — it contains your API credentials.
- **Never commit session files** — they provide full access to your Telegram account.
- **Never commit `chats.csv`** — it contains personal chat data.
- All three are excluded via `.gitignore`.
