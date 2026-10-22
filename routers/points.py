from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models.cliente import Cliente
from models.configuracion import ConfigPuntos, PuntosFacturaRegistrada
from pydantic import BaseModel

router = APIRouter(prefix="/points", tags=["Puntos y Facturas"])

class ScanFacturaSchema(BaseModel):
    numFactura: int
    idcliente: str

@router.post("/scan")
def escanear_y_acumular_factura(data: ScanFacturaSchema, db: Session = Depends(get_db)):
    # 1. Verificar si la factura existe en hfacturas de ExitoSystems
    factura_sql = text("SELECT numFactura, fecha, total, idcliente FROM hfacturas WHERE numFactura = :num")
    factura = db.execute(factura_sql, {"num": data.numFactura}).mappings().first()

    if not factura:
        raise HTTPException(status_code=404, detail="La factura no existe en el sistema.")

    # 2. Verificar que no haya sido registrada previamente para puntos
    ya_registrada = db.query(PuntosFacturaRegistrada).filter_by(numFactura=data.numFactura).first()
    if ya_registrada:
        raise HTTPException(status_code=400, detail="Esta factura ya fue registrada anteriormente y acumuló puntos.")

    # 3. Obtener el porcentaje de puntos configurado globalmente
    config = db.query(ConfigPuntos).first()
    porcentaje = float(config.porcentaje_puntos) if config else 5.00

    # 4. Consultar las líneas de la factura (lhfacturas) y filtrar productos excluidos
    query_detalles = text("""
        SELECT l.codigoProducto, l.total_linea 
        FROM lhfacturas l
        WHERE l.numFactura = :num 
          AND l.codigoProducto NOT IN (SELECT codigoProducto FROM productos_excluidos_puntos)
    """)

    try:
        detalles = db.execute(query_detalles, {"num": data.numFactura}).mappings().all()
    except Exception:
        detalles = []

    monto_elegible = sum(float(d["total_linea"]) for d in detalles) if detalles else float(factura["total"])

    # 5. Calcular los puntos obtenidos
    puntos_ganados = (monto_elegible * porcentaje) / 100.0

    # 6. Registrar en el historial de puntos y actualizar saldo del cliente en 'clientes.cuenta'
    cliente = db.query(Cliente).filter_by(idcliente=data.idcliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado en el sistema.")

    cuenta_actual = float(cliente.cuenta) if cliente.cuenta else 0.00
    cliente.cuenta = cuenta_actual + puntos_ganados

    nuevo_registro = PuntosFacturaRegistrada(
        numFactura=data.numFactura,
        idcliente=data.idcliente,
        monto_elegible=monto_elegible,
        puntos_otorgados=puntos_ganados
    )
    db.add(nuevo_registro)
    db.commit()

    return {
        "mensaje": "¡Puntos acumulados con éxito!",
        "numFactura": data.numFactura,
        "monto_elegible": monto_elegible,
        "puntos_otorgados": puntos_ganados,
        "nuevo_saldo_puntos": cliente.cuenta
    }