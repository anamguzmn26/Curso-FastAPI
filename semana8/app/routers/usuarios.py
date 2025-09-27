from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database.engine import get_db
from .. import models, schemas
from ..docs.descriptions import ENDPOINT_DESCRIPTIONS

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=schemas.UsuarioResponse, summary="Crear usuario",
             description=ENDPOINT_DESCRIPTIONS["crear_usuario"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = models.Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=List[schemas.UsuarioResponse], summary="Listar usuarios",
            description=ENDPOINT_DESCRIPTIONS["listar_usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()
