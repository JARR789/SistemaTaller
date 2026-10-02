from datetime import datetime, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .models import User, Session as UserSession

bearer = HTTPBearer()


def as_utc(value):
    """SQLite puede devolver DateTime sin tzinfo; las fechas almacenadas son UTC."""
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    try: payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError: raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    session = db.get(UserSession, payload.get("sid"))
    if not session or session.revoked_at or as_utc(session.expires_at) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Sesión cerrada o expirada")
    user = db.get(User, int(payload.get("sub", 0)))
    if not user or not user.is_active: raise HTTPException(status_code=403, detail="Usuario inactivo")
    return user

def require_roles(*allowed):
    def check(user: User = Depends(get_current_user)):
        if not set(allowed).intersection(role.name for role in user.roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permiso para esta acción")
        return user
    return check
