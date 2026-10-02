from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from pwdlib import PasswordHash
from .config import settings

password_hash = PasswordHash.recommended()
def hash_password(password: str) -> str: return password_hash.hash(password)
def verify_password(password: str, stored: str) -> bool: return password_hash.verify(password, stored)
def create_access_token(user_id: int, session_id: str) -> tuple[str, datetime]:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub": str(user_id), "sid": session_id, "exp": expires}, settings.jwt_secret, algorithm=settings.jwt_algorithm), expires
def new_session_id() -> str: return str(uuid4())
