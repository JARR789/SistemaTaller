"""Crea el administrador inicial desde consola; no expone una ruta pública."""
from getpass import getpass
from sqlalchemy import select
from .database import Base, engine, SessionLocal
from .models import Role, User
from .schemas import UserCreate
from .services.users import create_user

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    if db.scalar(select(User).join(User.roles).where(Role.name == "Administrador")):
        raise SystemExit("Ya existe un administrador.")
    username = input("Usuario administrador: ").strip()
    name = input("Nombre completo: ").strip()
    password = getpass("Contraseña: ")
    admin = create_user(db, UserCreate(username=username, full_name=name, password=password, roles=["Administrador"]))
    print(f"Administrador {admin.username} creado.")
finally:
    db.close()
