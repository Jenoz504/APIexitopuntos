from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.configuracion import ConfigPuntos, ProductosExcluidosPuntos
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Administración"])

class ConfigUpdateSchema(BaseModel):
    porcentaje_puntos: float
    monto_minimo_factura: float = 0.00

class ExcluirProductoSchema(BaseModel):
    codigoProducto: str

@router.get("/config")
def obtener_configuracion(db: Session = Depends(get_db)):
    config = db.query(ConfigPuntos).first()
    if not config:
        config = ConfigPuntos(porcentaje_puntos=5.00, monto_minimo_factura=0.00)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

@router.put("/config")
def actualizar_configuracion(data: ConfigUpdateSchema, db: Session = Depends(get_db)):
    config = db.query(ConfigPuntos).first()
    if not config:
        config = ConfigPuntos()
        db.add(config)
    
    config.porcentaje_puntos = data.porcentaje_puntos
    config.monto_minimo_factura = data.monto_minimo_factura
    db.commit()
    return {"mensaje": "Configuración actualizada exitosamente", "porcentaje": config.porcentaje_puntos}

@router.post("/productos-excluidos")
def excluir_producto(data: ExcluirProductoSchema, db: Session = Depends(get_db)):
    existente = db.query(ProductosExcluidosPuntos).filter_by(codigoProducto=data.codigoProducto).first()
    if existente:
        raise HTTPException(status_code=400, detail="El producto ya se encuentra excluido.")
    
    nuevo_excluido = ProductosExcluidosPuntos(codigoProducto=data.codigoProducto)
    db.add(nuevo_excluido)
    db.commit()
    return {"mensaje": f"Producto {data.codigoProducto} excluido correctamente."}