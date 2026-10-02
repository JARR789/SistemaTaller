from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import User, Role
from ..security import hash_password

def serialize(user: User) -> dict:
    return {"id": user.id, "username": user.username, "full_name": user.full_name, "is_active": user.is_active, "roles": [r.name for r in user.roles]}

def ensure_unique(db: Session, username: str | None, exclude_id: int | None = None):
    clauses = []
    if username: clauses.append(User.username == username.strip())
    if not clauses: return
    query = select(User).where(or_(*clauses))
    if exclude_id: query = query.where(User.id != exclude_id)
    if db.scalar(query): raise HTTPException(409, "El nombre de usuario ya está registrado")

def create_user(db: Session, data, roles: list[str] | None = None) -> User:
    ensure_unique(db, data.username)
    user = User(username=data.username.strip(), full_name=data.full_name.strip(), password_hash=hash_password(data.password))
    assigned = roles or data.roles
    user.roles = list(db.scalars(select(Role).where(Role.name.in_(assigned))).all())
    db.add(user); db.commit(); db.refresh(user)
    return user
