from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from . import schemas, services


router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.post(
    "/",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_201_CREATED,
)
def alta_venta(venta: schemas.VentaCreate):
    return services.crear(venta)


@router.get(
    "/",
    response_model=List[schemas.VentaRead],
    status_code=status.HTTP_200_OK,
)
def listar_ventas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    cliente: Optional[str] = Query(None),
    estado: Optional[schemas.EstadoVenta] = Query(None),
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
    monto_min: Optional[float] = Query(None, ge=0),
    monto_max: Optional[float] = Query(None, ge=0),
):
    return services.obtener_todas(
        skip=skip,
        limit=limit,
        cliente=cliente,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        monto_min=monto_min,
        monto_max=monto_max,
    )


@router.get(
    "/{id}",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def detalle_venta(id: int = Path(..., gt=0)):
    venta = services.obtener_por_id(id)

    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )

    return venta


@router.put(
    "/{id}",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def actualizar_venta(
    venta: schemas.VentaCreate,
    id: int = Path(..., gt=0),
):
    actualizada = services.actualizar_total(id, venta)

    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada o no se puede modificar",
        )

    return actualizada


@router.patch(
    "/{id}",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def actualizar_parcial_venta(
    venta: schemas.VentaUpdate,
    id: int = Path(..., gt=0),
):
    actualizada = services.actualizar_parcial(id, venta)

    if not actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada o no se puede modificar",
        )

    return actualizada


@router.put(
    "/{id}/desactivar",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivada = services.desactivar(id)

    if not desactivada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada o no se puede desactivar",
        )

    return desactivada


@router.put(
    "/{id}/confirmar",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def confirmar_venta(id: int = Path(..., gt=0)):
    confirmada = services.confirmar(id)

    if not confirmada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Venta no encontrada o no se puede confirmar",
        )

    return confirmada


@router.put(
    "/{id}/cancelar",
    response_model=schemas.VentaRead,
    status_code=status.HTTP_200_OK,
)
def cancelar_venta(id: int = Path(..., gt=0)):
    cancelada = services.cancelar(id)

    if not cancelada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Venta no encontrada o no se puede cancelar",
        )

    return cancelada