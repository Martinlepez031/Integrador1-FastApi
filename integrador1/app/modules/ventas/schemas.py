from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EstadoVenta(str, Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"


class VentaCreate(BaseModel):
    cliente: str = Field(..., min_length=2, max_length=100)
    producto: str = Field(..., min_length=2, max_length=100)
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)
    fecha: date
    estado: EstadoVenta = EstadoVenta.pendiente

    @field_validator("cliente", "producto")
    @classmethod
    def validar_textos(cls, valor: str):
        valor = valor.strip()

        if not valor:
            raise ValueError("El campo no puede estar vacío")

        return valor


class VentaUpdate(BaseModel):
    cliente: Optional[str] = Field(None, min_length=2, max_length=100)
    producto: Optional[str] = Field(None, min_length=2, max_length=100)
    cantidad: Optional[int] = Field(None, gt=0)
    precio_unitario: Optional[float] = Field(None, gt=0)
    fecha: Optional[date] = None
    estado: Optional[EstadoVenta] = None

    @field_validator("cliente", "producto")
    @classmethod
    def validar_textos(cls, valor: Optional[str]):
        if valor is None:
            return valor

        valor = valor.strip()

        if not valor:
            raise ValueError("El campo no puede estar vacío")

        return valor


class VentaRead(BaseModel):
    id: int
    cliente: str
    producto: str
    cantidad: int
    precio_unitario: float
    total: float
    fecha: date
    estado: EstadoVenta
    activo: bool