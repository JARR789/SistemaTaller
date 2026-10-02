from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user, require_roles
from ..models import User, Role
from ..schemas import AdminPasswordResetRequest, UserCreate, UserUpdate, UserOut, RoleAssignment
from ..security import hash_password
from ..services.users import create_user, ensure_unique, serialize

router = APIRouter(prefix="/users", tags=["Usuarios"])
admin = Depends(require_roles("Administrador"))

@router.get("", response_model=list[UserOut], dependencies=[admin])
def list_users(db: Session = Depends(get_db)): return [serialize(u) for u in db.scalars(select(User)).all()]

@router.post("", response_model=UserOut, status_code=201, dependencies=[admin])
def add_user(data: UserCreate, db: Session = Depends(get_db)): return serialize(create_user(db, data))

@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "Usuario no encontrado")
    is_admin = "Administrador" in [r.name for r in current.roles]
    if current.id != user_id and not is_admin: raise HTTPException(403, "No puede editar este usuario")
    if data.is_active is not None and not is_admin: raise HTTPException(403, "No puede cambiar el estado de una cuenta")
    values = data.model_dump(exclude_unset=True)
    ensure_unique(db, values.get("username"), user_id)
    for key, value in values.items(): setattr(user, key, value.strip() if isinstance(value, str) else value)
    db.commit(); db.refresh(user); return serialize(user)

@router.put("/{user_id}/roles", response_model=UserOut, dependencies=[admin])
def set_roles(user_id: int, data: RoleAssignment, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "Usuario no encontrado")
    roles = list(db.scalars(select(Role).where(Role.name.in_(data.roles))).all())
    if len(roles) != len(data.roles): raise HTTPException(400, "Uno o más roles no existen")
    user.roles = roles; db.commit(); db.refresh(user); return serialize(user)


@router.put("/{user_id}/reset-password", status_code=204, dependencies=[admin])
def reset_password(user_id: int, data: AdminPasswordResetRequest, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "Usuario no encontrado")
    user.password_hash = hash_password(data.new_password)
    for session in user.sessions:
        session.revoked_at = datetime.now(timezone.utc)
    db.commit()
