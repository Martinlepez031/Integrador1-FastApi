from datetime import date
from typing import List, Optional

from .schemas import VentaCreate, VentaUpdate, VentaRead, EstadoVenta


ventas: List[VentaRead] = []
contador_id = 1


def calcular_total(cantidad: int, precio_unitario: float) -> float:
    return cantidad * precio_unitario


def crear(venta: VentaCreate) -> VentaRead:
    global contador_id

    total = calcular_total(venta.cantidad, venta.precio_unitario)

    nueva_venta = VentaRead(
        id=contador_id,
        cliente=venta.cliente,
        producto=venta.producto,
        cantidad=venta.cantidad,
        precio_unitario=venta.precio_unitario,
        total=total,
        fecha=venta.fecha,
        estado=venta.estado,
        activo=True,
    )

    ventas.append(nueva_venta)
    contador_id += 1

    return nueva_venta


def obtener_todas(
    skip: int = 0,
    limit: int = 10,
    cliente: Optional[str] = None,
    estado: Optional[EstadoVenta] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    monto_min: Optional[float] = None,
    monto_max: Optional[float] = None,
) -> List[VentaRead]:

    resultado = [venta for venta in ventas if venta.activo]

    if cliente:
        resultado = [
            venta for venta in resultado
            if cliente.lower() in venta.cliente.lower()
        ]

    if estado:
        resultado = [
            venta for venta in resultado
            if venta.estado == estado
        ]

    if fecha_desde:
        resultado = [
            venta for venta in resultado
            if venta.fecha >= fecha_desde
        ]

    if fecha_hasta:
        resultado = [
            venta for venta in resultado
            if venta.fecha <= fecha_hasta
        ]

    if monto_min is not None:
        resultado = [
            venta for venta in resultado
            if venta.total >= monto_min
        ]

    if monto_max is not None:
        resultado = [
            venta for venta in resultado
            if venta.total <= monto_max
        ]

    return resultado[skip: skip + limit]


def obtener_por_id(id: int) -> Optional[VentaRead]:
    for venta in ventas:
        if venta.id == id and venta.activo:
            return venta

    return None


def actualizar_total(id: int, venta_actualizada: VentaCreate) -> Optional[VentaRead]:
    for index, venta in enumerate(ventas):
        if venta.id == id and venta.activo:

            if venta.estado == EstadoVenta.confirmada:
                return None

            if venta.estado == EstadoVenta.cancelada:
                return None

            total = calcular_total(
                venta_actualizada.cantidad,
                venta_actualizada.precio_unitario
            )

            ventas[index] = VentaRead(
                id=id,
                cliente=venta_actualizada.cliente,
                producto=venta_actualizada.producto,
                cantidad=venta_actualizada.cantidad,
                precio_unitario=venta_actualizada.precio_unitario,
                total=total,
                fecha=venta_actualizada.fecha,
                estado=venta_actualizada.estado,
                activo=True,
            )

            return ventas[index]

    return None


def actualizar_parcial(id: int, datos: VentaUpdate) -> Optional[VentaRead]:
    for index, venta in enumerate(ventas):
        if venta.id == id and venta.activo:

            if venta.estado == EstadoVenta.confirmada:
                return None

            if venta.estado == EstadoVenta.cancelada:
                return None

            datos_actualizados = venta.model_dump()
            nuevos_datos = datos.model_dump(exclude_unset=True)

            datos_actualizados.update(nuevos_datos)

            datos_actualizados["total"] = calcular_total(
                datos_actualizados["cantidad"],
                datos_actualizados["precio_unitario"]
            )

            ventas[index] = VentaRead(**datos_actualizados)

            return ventas[index]

    return None


def desactivar(id: int) -> Optional[VentaRead]:
    for index, venta in enumerate(ventas):
        if venta.id == id and venta.activo:

            if venta.estado == EstadoVenta.confirmada:
                return None

            venta_desactivada = venta.model_copy(update={"activo": False})
            ventas[index] = venta_desactivada

            return venta_desactivada

    return None


def confirmar(id: int) -> Optional[VentaRead]:
    for index, venta in enumerate(ventas):
        if venta.id == id and venta.activo:

            if venta.estado == EstadoVenta.cancelada:
                return None

            venta_confirmada = venta.model_copy(
                update={"estado": EstadoVenta.confirmada}
            )

            ventas[index] = venta_confirmada

            return venta_confirmada

    return None


def cancelar(id: int) -> Optional[VentaRead]:
    for index, venta in enumerate(ventas):
        if venta.id == id and venta.activo:

            if venta.estado == EstadoVenta.confirmada:
                return None

            venta_cancelada = venta.model_copy(
                update={"estado": EstadoVenta.cancelada}
            )

            ventas[index] = venta_cancelada

            return venta_cancelada

    return None