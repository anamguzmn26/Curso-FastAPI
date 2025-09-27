from fastapi import FastAPI
from app.routers import usuarios
from app.docs.descriptions import ENDPOINT_DESCRIPTIONS  # opcional
from app.docs.descriptions import ENDPOINT_DESCRIPTIONS
from app import __version__

TAGS_METADATA = [
    {
        "name": "usuarios",
        "description": "Operaciones CRUD para usuarios del sistema Autolavado Premium CleanCar."
    },
    {
        "name": "auth",
        "description": "Registro e inicio de sesión de usuarios."
    },
]

app = FastAPI(
    title="Autolavado Premium CleanCar API",
    version="0.1.0",
    openapi_tags=TAGS_METADATA
)

app.include_router(usuarios.router, tags=["usuarios"])
# si tienes router auth:
# app.include_router(auth.router, tags=["auth"])
