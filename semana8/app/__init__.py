from fastapi import FastAPI
from app.routers import usuarios

app = FastAPI(title="Autolavado Premium CleanCar API")

app.include_router(usuarios.router)

# opcional: endpoints de auth
