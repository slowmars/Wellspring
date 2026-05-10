import os
import json
import base64
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

VOLUNTEER_PW = os.getenv("DEMO_VOLUNTEER_PW", "volunteer123")
STAFF_PW = os.getenv("DEMO_STAFF_PW", "staff123")


def make_token(role: str) -> str:
    payload = json.dumps({"role": role})
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_token(token: str) -> dict:
    try:
        payload = base64.urlsafe_b64decode(token.encode()).decode()
        return json.loads(payload)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_auth(x_auth_token: str = Header(..., alias="X-Auth-Token")) -> dict:
    data = decode_token(x_auth_token)
    if "role" not in data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return data


def require_staff(x_auth_token: str = Header(..., alias="X-Auth-Token")) -> dict:
    data = decode_token(x_auth_token)
    if data.get("role") != "staff":
        raise HTTPException(status_code=403, detail="Staff access required")
    return data

from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
