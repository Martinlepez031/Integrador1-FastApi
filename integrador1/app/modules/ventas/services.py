from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from .schemas import VentaCreate, VentaUpdate, EstadoVenta
from .models import Venta


def calcular_total(cantidad: int, precio_unitario: float) -> float:
    return cantidad * precio_unitario


def crear(db: Session, venta: VentaCreate) -> Venta:
    total = calcular_total(venta.cantidad, venta.precio_unitario)

    nueva_venta = Venta(
        cliente=venta.cliente,
        producto=venta.producto,
        cantidad=venta.cantidad,
        precio_unitario=venta.precio_unitario,
        total=total,
        fecha=venta.fecha,
        estado=venta.estado,
        activo=True,
    )

    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    return nueva_venta


def obtener_todas(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    cliente: Optional[str] = None,
    estado: Optional[EstadoVenta] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    monto_min: Optional[float] = None,
    monto_max: Optional[float] = None,
) -> List[Venta]:

    query = db.query(Venta).filter(Venta.activo == True)

    if cliente:
        query = query.filter(Venta.cliente.ilike(f"%{cliente}%"))

    if estado:
        query = query.filter(Venta.estado == estado)

    if fecha_desde:
        query = query.filter(Venta.fecha >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Venta.fecha <= fecha_hasta)

    if monto_min is not None:
        query = query.filter(Venta.total >= monto_min)

    if monto_max is not None:
        query = query.filter(Venta.total <= monto_max)

    return query.offset(skip).limit(limit).all()


def obtener_por_id(db: Session, id: int) -> Optional[Venta]:
    return db.query(Venta).filter(
        Venta.id == id,
        Venta.activo == True
    ).first()


def actualizar_total(
    db: Session,
    id: int,
    venta_actualizada: VentaCreate
) -> Optional[Venta]:

    venta = obtener_por_id(db, id)

    if not venta:
        return None

    if venta.estado == EstadoVenta.confirmada:
        return None

    if venta.estado == EstadoVenta.cancelada:
        return None

    venta.cliente = venta_actualizada.cliente
    venta.producto = venta_actualizada.producto
    venta.cantidad = venta_actualizada.cantidad
    venta.precio_unitario = venta_actualizada.precio_unitario
    venta.total = calcular_total(
        venta_actualizada.cantidad,
        venta_actualizada.precio_unitario
    )
    venta.fecha = venta_actualizada.fecha
    venta.estado = venta_actualizada.estado
    venta.activo = True

    db.commit()
    db.refresh(venta)

    return venta


def actualizar_parcial(
    db: Session,
    id: int,
    datos: VentaUpdate
) -> Optional[Venta]:

    venta = obtener_por_id(db, id)

    if not venta:
        return None

    if venta.estado == EstadoVenta.confirmada:
        return None

    if venta.estado == EstadoVenta.cancelada:
        return None

    nuevos_datos = datos.model_dump(exclude_unset=True)

    for campo, valor in nuevos_datos.items():
        setattr(venta, campo, valor)

    venta.total = calcular_total(
        venta.cantidad,
        venta.precio_unitario
    )

    db.commit()
    db.refresh(venta)

    return venta


def desactivar(db: Session, id: int) -> Optional[Venta]:
    venta = obtener_por_id(db, id)

    if not venta:
        return None

    if venta.estado == EstadoVenta.confirmada:
        return None

    venta.activo = False

    db.commit()
    db.refresh(venta)

    return venta


def confirmar(db: Session, id: int) -> Optional[Venta]:
    venta = obtener_por_id(db, id)

    if not venta:
        return None

    if venta.estado == EstadoVenta.cancelada:
        return None

    venta.estado = EstadoVenta.confirmada

    db.commit()
    db.refresh(venta)

    return venta


def cancelar(db: Session, id: int) -> Optional[Venta]:
    venta = obtener_por_id(db, id)

    if not venta:
        return None

    if venta.estado == EstadoVenta.confirmada:
        return None

    venta.estado = EstadoVenta.cancelada

    db.commit()
    db.refresh(venta)

    return venta