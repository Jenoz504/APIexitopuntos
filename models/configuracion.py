from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship


class ConfigPuntos(Base):
  __tablename__ = "config_puntos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  porcentaje_puntos = Column(Numeric(5, 2), default=5.00)
  monto_minimo_factura = Column(Numeric(15, 2), default=0.00)
  actualizado_el = Column(
      DateTime, server_default=func.now(), onupdate=func.now()
  )


class ProductosExcluidosPuntos(Base):
  __tablename__ = "productos_excluidos_puntos"

  codigoProducto = Column(String(30), primary_key=True)


class PuntosFacturaRegistrada(Base):
  __tablename__ = "puntos_facturas_registradas"

  id = Column(Integer, primary_key=True, autoincrement=True)
  numFactura = Column(Integer, unique=True, nullable=False)
  idcliente = Column(String(25), nullable=False)
  monto_elegible = Column(Numeric(15, 2), nullable=False)
  puntos_otorgados = Column(Numeric(15, 2), nullable=False)
  fecha_registro = Column(DateTime, server_default=func.now())