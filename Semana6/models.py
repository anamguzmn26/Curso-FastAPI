from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Rental(Base):
    __tablename__ = "rental_alquilers"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    vehiculo = Column(String, index=True)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    precio_diario = Column(Integer)
    licencia_valida = Column(Boolean, default=True)
    edad_conductor = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ej: admin_rental, cliente_rental, empleado_rental
    is_active = Column(Boolean, default=True)