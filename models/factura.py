from database import Base
from sqlalchemy import Column, Date, DateTime, Decimal, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship

class HFactura(Base):
  __tablename__ = "hfacturas"

  numFactura = Column(Integer, primary_key=True, index=True)
  idcliente = Column(String(25), ForeignKey("clientes.idcliente"), nullable=True)
  fecha = Column(String(45), nullable=True)
  subtotal = Column(Numeric(17, 2), default=0.00)
  total = Column(Numeric(15, 2), default=0.00)
  estado = Column(Integer, nullable=True)

  # Relaciones
  lineas = relationship("LHFactura", back_populates="factura")
  movimientos = relationship("Movimiento", back_populates="factura")

  class LHFactura(Base):
  __tablename__ = "lhfacturas"

  id = Column(Integer, primary_key=True, autoincrement=True)
  codigoProducto = Column(String(30), ForeignKey("inventario.codigoProducto"), nullable=True)
  numFactura = Column(Integer, ForeignKey("hfacturas.numFactura"), nullable=False)
  precio = Column(Numeric(17, 2), nullable=True)
  cantidad = Column(Numeric(17, 2), default=1.00)
  total_linea = Column(Numeric(17, 2), default=0.00)

  # Relaciones
  factura = relationship("HFactura", back_populates="lineas")