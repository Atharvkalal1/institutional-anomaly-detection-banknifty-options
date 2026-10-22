import base64
import hashlib
import json
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv
from fyers_apiv3 import fyersModel
import os


DATA_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DATA_DIR.parent

# .env exists in project root 
load_dotenv(PROJECT_ROOT / ".env")

# --- Configuration ---
APP_ID = os.getenv("FYERS_APP_ID")
SECRET_KEY = os.getenv("FYERS_SECRET_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PIN = os.getenv("FYERS_PIN")  # 4-digit trading PIN, needed only for refresh

TOKEN_PATH = DATA_DIR / "access_token.txt"
REFRESH_TOKEN_PATH = DATA_DIR / "refresh_token.txt"

REFRESH_URL = "https://api-t1.fyers.in/api/v3/validate-refresh-token"

if not all([APP_ID, SECRET_KEY, REDIRECT_URI]):
    raise SystemExit(
        "Missing FYERS_APP_ID / FYERS_SECRET_KEY / REDIRECT_URI in data/.env"
    )


# --- Small helpers -----------------------------------------------------

def _decode_jwt_expiry(token: str) -> Optional[datetime]:
    """Read the 'exp' claim out of a JWT without verifying its signature."""
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)  # fix padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        exp = payload.get("exp")
        return datetime.fromtimestamp(exp, tz=timezone.utc) if exp else None
    except Exception:
        return None


def _is_token_valid(token: Optional[str], leeway_seconds: int = 300) -> bool:
    """True if `token` decodes as a JWT and isn't expired (with a safety margin)."""
    if not token:
        return False
    expiry = _decode_jwt_expiry(token)
    if expiry is None:
        return False
    return datetime.now(timezone.utc) < (expiry - timedelta(seconds=leeway_seconds))


def _read(path: Path) -> Optional[str]:
    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        return text or None
    return None


def _write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


# --- Token generation / refresh ----------------------------------------

def generate_access_token() -> Optional[str]:
    """Full browser login flow. Saves both access_token and refresh_token."""
    session = fyersModel.SessionModel(
        client_id=APP_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code",
    )

    auth_url = session.generate_authcode()
    print("Opening browser for FYERS login...")
    webbrowser.open(auth_url)

    print("\n1. Log in via the browser window.")
    print("2. After success, copy the 'auth_code' parameter from the redirected URL bar.")
    auth_code = input("\nPaste the auth_code here: ").strip()

    session.set_token(auth_code)
    response = session.generate_token()

    if response.get("s") != "ok":
        print(f"\nFailed to generate token: {response}")
        return None

    access_token = response["access_token"]
    refresh_token = response.get("refresh_token")

    print("\nSUCCESS! Your Access Token:")
    print(access_token)

    _write(TOKEN_PATH, access_token)
    print(f"Saved access token to '{TOKEN_PATH}'.")

    if refresh_token:
        _write(REFRESH_TOKEN_PATH, refresh_token)
        print(f"Saved refresh token to '{REFRESH_TOKEN_PATH}'.")

    return access_token


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """Exchange a still-valid refresh_token for a new access_token, no browser needed."""
    if not PIN:
        print("FYERS_PIN not set in .env -- cannot use refresh_token, falling back to login.")
        return None

    app_id_hash = hashlib.sha256(f"{APP_ID}:{SECRET_KEY}".encode()).hexdigest()
    payload = {
        "grant_type": "refresh_token",
        "appIdHash": app_id_hash,
        "refresh_token": refresh_token,
        "pin": PIN,
    }

    try:
        resp = requests.post(REFRESH_URL, json=payload, timeout=15)
        data = resp.json()
    except Exception as exc:
        print(f"Refresh request failed: {exc}")
        return None

    if data.get("s") != "ok":
        print(f"Refresh failed: {data}")
        return None

    access_token = data["access_token"]
    print("Refreshed access token using refresh_token (no browser login needed).")
    _write(TOKEN_PATH, access_token)
    return access_token


def get_valid_access_token() -> Optional[str]:
    """
    Main entry point:
    1. Reuse the saved access_token if it isn't expired.
    2. Otherwise, try to refresh it using the saved refresh_token.
    3. Otherwise, fall back to full browser login.
    """
    access_token = _read(TOKEN_PATH)
    if _is_token_valid(access_token):
        print("Existing access token is still valid.")
        return access_token

    refresh_token = _read(REFRESH_TOKEN_PATH)
    if refresh_token:
        new_token = refresh_access_token(refresh_token)
        if new_token:
            return new_token
        print("Refresh token unusable/expired -- doing a fresh login.")

    return generate_access_token()


if __name__ == "__main__":
    get_valid_access_token()
