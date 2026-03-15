import os
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict:
    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    session_name = os.getenv("TG_SESSION_NAME")

    missing = [k for k, v in {"TG_API_ID": api_id, "TG_API_HASH": api_hash, "TG_SESSION_NAME": session_name}.items() if not v]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return {
        "api_id": int(api_id),
        "api_hash": api_hash,
        "session_name": session_name,
    }
