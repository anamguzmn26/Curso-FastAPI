from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Rental
from schemas import RentalCreate, RentalUpdate, RentalOut
from database import get_db
from datetime import date
from routers.auth import get_current_active_user

router = APIRouter(
    prefix="/rental_alquilers",
    tags=["rental"]
)

@router.post("/", response_model=RentalOut, status_code=201)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    # Validaciones de negocio
    if rental.edad_conductor < 21:
        raise HTTPException(status_code=422, detail="La edad mínima es 21 años")
    if rental.fecha_fin < rental.fecha_inicio:
        raise HTTPException(status_code=422, detail="La fecha fin no puede ser anterior a inicio")

    db_rental = Rental(**rental.dict())
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

@router.get("/{rental_id}", response_model=RentalOut)
def get_rental(rental_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not db_rental:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return db_rental

@router.put("/{rental_id}", response_model=RentalOut)
def update_rental(rental_id: int, rental: RentalUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not db_rental:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    for key, value in rental.dict().items():
        setattr(db_rental, key, value)

    db.commit()
    db.refresh(db_rental)
    return db_rental

@router.delete("/{rental_id}")
def delete_rental(rental_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if not db_rental:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    # Solo admin puede eliminar
    if current_user.role != "admin_rental":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    db.delete(db_rental)
    db.commit()
    return {"message": "Alquiler eliminado"}