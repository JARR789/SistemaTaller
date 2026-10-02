# Módulo de identidad — Taller Mecánico

SPA de Vue 3 + Vuetify y API de FastAPI para cuentas, roles, autenticación y sesiones.

## Arranque local en Windows / VS Code

Requiere Python 3.11+ y Node.js LTS con npm. Abra dos terminales integradas de VS Code en la carpeta raíz del proyecto.

**Terminal 1 — API**

```powershell
cd backend
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m app.seed_admin
uvicorn app.main:app --reload --port 8000
```

El asistente de `seed_admin` solicita usuario, correo, nombre y contraseña. La contraseña debe tener 10 caracteres o más, con mayúscula, minúscula y número. No comparta estas credenciales.

**Terminal 2 — SPA**

```powershell
cd frontend
npm install
npm run dev
```

Abra la dirección mostrada por Vite, normalmente `http://localhost:5173`. Inicie sesión con el usuario o correo y la contraseña creados por `seed_admin`.

Para probar el registro público, cree una cuenta desde **Crear cuenta**; recibirá únicamente el rol `Cliente`. Inicie sesión con ella después del registro. Desde la sesión de administrador, entre en **Usuarios** para crear personal y asignar los demás roles.

## Seguridad aplicada

- Argon2 con sal individual por contraseña (`pwdlib`), sin secretos ni contraseñas en texto plano.
- Índices únicos para correo y usuario en la base de datos, además de validación previa de la API.
- JWT breve ligado a una sesión persistida; logout, inactividad y restablecimiento invalidan sesiones.
- Validación de payloads y permisos en FastAPI, además de validaciones de formulario y guardas del router.
- Recuperación de contraseña anti-enumeración. Debe conectarse un proveedor de correo donde se indica en `auth.py`; no se expone ni registra el token.
- Configure una `JWT_SECRET` larga y única y `DATABASE_URL` de SQL Server antes de producción.
