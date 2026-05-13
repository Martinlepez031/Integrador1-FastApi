from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from . import schemas, services


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "/",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_201_CREATED
)
def alta_producto(
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db)
):
    return services.crear(db, producto)


@router.get(
    "/",
    response_model=List[schemas.ProductoRead],
    status_code=status.HTTP_200_OK
)
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    return services.obtener_todos(db, skip, limit)


@router.get(
    "/{id}",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK
)
def detalle_producto(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    producto = services.obtener_por_id(db, id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto


@router.put(
    "/{id}",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK
)
def actualizar_producto(
    producto: schemas.ProductoCreate,
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    actualizado = services.actualizar_total(db, id, producto)

    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return actualizado


@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    desactivado = services.desactivar(db, id)

    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return desactivado


@router.get(
    "/{id}/stock",
    response_model=schemas.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
def consultar_stock(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    resultado = services.obtener_estado_stock(db, id)

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return resultado