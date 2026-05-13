from typing import List, Optional
from sqlalchemy.orm import Session

from .schemas import CategoriaCreate
from .models import Categoria


def crear(db: Session, data: CategoriaCreate) -> Categoria:
    nueva = Categoria(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def obtener_todas(db: Session, skip: int = 0, limit: int = 10) -> List[Categoria]:
    return db.query(Categoria).offset(skip).limit(limit).all()


def obtener_por_id(db: Session, id: int) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id == id).first()


def actualizar_total(db: Session, id: int, data: CategoriaCreate) -> Optional[Categoria]:
    categoria = obtener_por_id(db, id)

    if not categoria:
        return None

    categoria.codigo = data.codigo
    categoria.descripcion = data.descripcion
    categoria.activo = data.activo

    db.commit()
    db.refresh(categoria)

    return categoria


def desactivar(db: Session, id: int) -> Optional[Categoria]:
    categoria = obtener_por_id(db, id)

    if not categoria:
        return None

    categoria.activo = False

    db.commit()
    db.refresh(categoria)

    return categoria