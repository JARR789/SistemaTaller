# Plan de estructura base — Taller Mecánico

Estado revisado: 2 de octubre de 2026.

## Fases y módulos

| Fase | Módulo | Estado | Alcance actual |
|---|---|---|---|
| 1 | Estructura técnica base | Terminado | SPA Vue 3 + Vuetify, API FastAPI, configuración de base de datos y separación por rutas, modelos, esquemas, servicios y seguridad. |
| 2 | Identidad y autenticación | Terminado | Registro, login, logout, hash Argon2, sesiones JWT, cambio de contraseña y validaciones de credenciales. |
| 3 | Usuarios y roles | Terminado | Alta de usuarios con rol obligatorio, cinco roles disponibles, edición, activación de cuenta, autorización de API y protección de rutas SPA. |
| 4 | Recuperación de acceso | Terminado | Solicitud de recuperación y restablecimiento administrado de contraseña; invalida sesiones existentes. |
| 5 | Órdenes de reparación | Pendiente | Alta, edición, consulta, folios, cliente, vehículo, diagnóstico, mano de obra, piezas y totales. |
| 6 | Catálogo de clientes y vehículos | Pendiente | Clientes, vehículos, relación cliente-vehículo e historial de servicios. |
| 7 | Flujo operativo de taller | Pendiente | Asignación a técnico, fases de trabajo, bitácora, evidencias, tiempos y cambios de estado. |
| 8 | Consulta de cliente | Pendiente | Portal restringido para consultar el estado de una orden y el avance del vehículo. |
| 9 | Reportes y seguimiento | Pendiente | Indicadores operativos, órdenes por estado, carga de técnicos e historial. |
| 10 | Producción y calidad | Pendiente | Migraciones SQL Server, auditoría, pruebas automatizadas, correo/SMS si se requiere, respaldo y despliegue. |

## Roles habilitados

| Rol | Alta inicial | Acceso actual |
|---|---|---|
| Administrador | Sí | Usuarios, roles y administración completa. |
| Recepcionista | Sí | Identidad creada; módulo operativo pendiente. |
| Asesor de servicio | Sí | Identidad creada; módulo operativo pendiente. |
| Técnico | Sí | Identidad creada; módulo operativo pendiente. |
| Cliente | Sí | Identidad creada; consulta de órdenes pendiente. |

## Criterios para la siguiente fase

1. Definir los campos exactos de una orden de reparación y sus estados.
2. Crear modelos SQL Server para clientes, vehículos y órdenes.
3. Implementar las rutas FastAPI y vistas Vue para recepción y asesor de servicio.
4. Aplicar autorización por rol en cada operación, no sólo en el menú.

## Gestión de dependencias

El entorno virtual actual funciona con `pip`. Cuando la conexión a PyPI esté disponible, instale `uv` dentro del backend con:

```powershell
.\backend\.venv\Scripts\python.exe -m pip install uv
.\backend\.venv\Scripts\uv.exe --version
```
