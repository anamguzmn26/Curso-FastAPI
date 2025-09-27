from pydantic import BaseModel
from datetime import date
from typing import Optional

# Rental schemas
class RentalBase(BaseModel):
    cliente: str
    vehiculo: str
    fecha_inicio: date
    fecha_fin: date
    precio_diario: int
    licencia_valida: bool
    edad_conductor: int

class RentalCreate(RentalBase):
    pass

class RentalUpdate(RentalBase):
    pass

class RentalOut(RentalBase):
    id: int

    class Config:
        orm_mode = True

# User / Auth schemas
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None