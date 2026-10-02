from datetime import datetime, timedelta, timezone
import hashlib, secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user, bearer
from ..models import User, Session as UserSession, PasswordResetToken
from ..schemas import LoginRequest, TokenOut, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest, UserCreate, UserOut
from ..security import verify_password, hash_password, create_access_token, new_session_id
from ..services.users import create_user, serialize
from ..dependencies import as_utc

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return serialize(create_user(db, data))

@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    value = data.username.strip()
    user = db.scalar(select(User).where(User.username == value))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    if not user.is_active: raise HTTPException(403, "Usuario inactivo")
    session_id = new_session_id(); token, expires = create_access_token(user.id, session_id)
    db.add(UserSession(id=session_id, user_id=user.id, expires_at=expires)); db.commit()
    return {"access_token": token, "user": serialize(user)}

@router.post("/logout", status_code=204)
def logout(credentials=Depends(bearer), user=Depends(get_current_user), db: Session = Depends(get_db)):
    import jwt
    from ..config import settings
    payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    session = db.get(UserSession, payload["sid"])
    session.revoked_at = datetime.now(timezone.utc); db.commit()

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)): return serialize(user)

@router.post("/forgot-password", status_code=202)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == data.username.strip()))
    # Siempre respondemos igual para no revelar cuentas existentes.
    if user:
        raw = secrets.token_urlsafe(48)
        db.add(PasswordResetToken(user_id=user.id, token_hash=hashlib.sha256(raw.encode()).hexdigest(), expires_at=datetime.now(timezone.utc)+timedelta(minutes=30)))
        db.commit()
        # El token se entrega únicamente mediante un canal de recuperación configurado por el taller.
    return {"message": "Si el usuario existe, el administrador podrá gestionar la recuperación de forma segura."}

@router.post("/reset-password", status_code=204)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    token = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token_hash == hashlib.sha256(data.token.encode()).hexdigest()))
    if not token or token.used_at or as_utc(token.expires_at) < datetime.now(timezone.utc): raise HTTPException(400, "El enlace de recuperación es inválido o expiró")
    user = db.get(User, token.user_id); user.password_hash = hash_password(data.new_password); token.used_at = datetime.now(timezone.utc)
    for session in user.sessions: session.revoked_at = datetime.now(timezone.utc)
    db.commit()

@router.post("/change-password", status_code=204)
def change_password(data: ChangePasswordRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(data.current_password, user.password_hash): raise HTTPException(400, "La contraseña actual no es correcta")
    user.password_hash = hash_password(data.new_password)
    db.commit()
