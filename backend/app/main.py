from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, select, text
from .config import settings
from .database import Base, engine, SessionLocal
from .models import Role
from .routes import auth, users

def migrate_legacy_sqlite_schema():
    """Migra la base local inicial, preservando datos, al modelo sin correo."""
    if engine.dialect.name != "sqlite":
        return
    if "users" not in inspect(engine).get_table_names():
        return
    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    if "email" not in columns:
        return
    with engine.connect() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
        connection.execute(text("""
            CREATE TABLE users_without_email (
                id INTEGER NOT NULL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                full_name VARCHAR(120) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL
            )
        """))
        connection.execute(text("""
            INSERT INTO users_without_email (id, username, full_name, password_hash, is_active, created_at)
            SELECT id, username, full_name, password_hash, is_active, created_at FROM users
        """))
        connection.execute(text("DROP TABLE users"))
        connection.execute(text("ALTER TABLE users_without_email RENAME TO users"))
        connection.commit()
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    migrate_legacy_sqlite_schema()
    db = SessionLocal()
    try:
        for name in ["Administrador", "Recepcionista", "Asesor de servicio", "Técnico", "Cliente"]:
            if not db.scalar(select(Role).where(Role.name == name)): db.add(Role(name=name))
        db.commit()
    finally: db.close()
    yield

app = FastAPI(title="Taller Mecánico API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_url], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.get("/health")
def health(): return {"status": "ok"}
