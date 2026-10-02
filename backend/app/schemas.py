from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

ROLES = {"Administrador", "Recepcionista", "Asesor de servicio", "Técnico", "Cliente"}


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    full_name: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=10, max_length=128)
    roles: list[str] = Field(min_length=1)

    @field_validator("password")
    @classmethod
    def strong_password(cls, value):
        if not any(c.isupper() for c in value) or not any(c.islower() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número")
        return value

    @field_validator("roles")
    @classmethod
    def valid_roles(cls, values):
        if not set(values).issubset(ROLES):
            raise ValueError("Rol no permitido")
        return list(dict.fromkeys(values))


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    full_name: str | None = Field(default=None, min_length=3, max_length=120)
    is_active: bool | None = None


class RoleAssignment(BaseModel):
    roles: list[str] = Field(min_length=1)
    @field_validator("roles")
    @classmethod
    def valid_roles(cls, values):
        if not set(values).issubset(ROLES): raise ValueError("Rol no permitido")
        return list(dict.fromkeys(values))


class UserOut(BaseModel):
    id: int; username: str; full_name: str; is_active: bool; roles: list[str]
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class TokenOut(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut


class ForgotPasswordRequest(BaseModel): username: str = Field(min_length=3, max_length=50)
class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=32, max_length=200)
    new_password: str = Field(min_length=10, max_length=128)
    @field_validator("new_password")
    @classmethod
    def strong_password(cls, value):
        return UserCreate.strong_password(value)

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=10, max_length=128)
    @field_validator("new_password")
    @classmethod
    def strong_password(cls, value):
        return UserCreate.strong_password(value)


class AdminPasswordResetRequest(BaseModel):
    new_password: str = Field(min_length=10, max_length=128)

    @field_validator("new_password")
    @classmethod
    def strong_password(cls, value):
        return UserCreate.strong_password(value)
