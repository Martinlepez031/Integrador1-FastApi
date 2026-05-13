from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from . import schemas, services


router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post(
    "/",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_201_CREATED
)
def alta_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db)
):
    return services.crear(db, categoria)


@router.get(
    "/",
    response_model=List[schemas.CategoriaRead],
    status_code=status.HTTP_200_OK
)
def listar_categorias(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    return services.obtener_todas(db, skip, limit)


@router.get(
    "/{id}",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK
)
def detalle_categoria(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    categoria = services.obtener_por_id(db, id)

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return categoria


@router.put(
    "/{id}",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK
)
def actualizar_categoria(
    categoria: schemas.CategoriaCreate,
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    actualizada = services.actualizar_total(db, id, categoria)

    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return actualizada


@router.put(
    "/{id}/desactivar",
    response_model=schemas.CategoriaRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    desactivada = services.desactivar(db, id)

    if not desactivada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return desactivada