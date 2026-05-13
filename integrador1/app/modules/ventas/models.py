from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy import Enum as SqlEnum

from app.core.database import Base
from .schemas import EstadoVenta


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(100), nullable=False)
    producto = Column(String(100), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(SqlEnum(EstadoVenta), default=EstadoVenta.pendiente, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)