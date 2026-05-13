from typing import List, Optional
from sqlalchemy.orm import Session

from .schemas import ProductoCreate
from .models import Producto


def crear(db: Session, data: ProductoCreate) -> Producto:
    nuevo = Producto(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


def obtener_todos(db: Session, skip: int, limit: int) -> List[Producto]:
    return db.query(Producto).offset(skip).limit(limit).all()


def obtener_por_id(db: Session, id: int) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id == id).first()


def actualizar_total(db: Session, id: int, data: ProductoCreate) -> Optional[Producto]:
    producto = obtener_por_id(db, id)

    if not producto:
        return None

    producto.nombre = data.nombre
    producto.categoria = data.categoria
    producto.precio = data.precio
    producto.stock = data.stock
    producto.stock_minimo = data.stock_minimo
    producto.activo = data.activo

    db.commit()
    db.refresh(producto)

    return producto


def desactivar(db: Session, id: int) -> Optional[Producto]:
    producto = obtener_por_id(db, id)

    if not producto:
        return None

    producto.activo = False

    db.commit()
    db.refresh(producto)

    return producto


def obtener_estado_stock(db: Session, id: int) -> Optional[dict]:
    producto = obtener_por_id(db, id)

    if not producto:
        return None

    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }