from fastapi import FastAPI
from database import Base, engine, get_db   # 👈 añadimos get_db aquí
from routers import rental, auth

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rent a Car - API")

# Incluir routers
app.include_router(auth.router)
app.include_router(rental.router)

@app.get("/")
def root():
    return {"message": "API Rent a Car funcionando 🚗"}

# 👇 esto resuelve el ImportError
__all__ = ["app", "get_db"]