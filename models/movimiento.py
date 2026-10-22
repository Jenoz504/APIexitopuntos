from database import Base
from sqlalchemy import Column, Date, DateTime, Decimal, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship

class Movimiento(Base):
  __tablename__ = "movimientos"

  idmovimientos = Column(
      Integer, primary_key=True, autoincrement=True, index=True
  )
  idcliente = Column(String(25), ForeignKey("clientes.idcliente"), nullable=True)
  idfactura = Column(Integer, ForeignKey("hfacturas.numFactura"), nullable=True)
  tipo_movimiento = Column(Integer, nullable=True)
  monto = Column(Numeric(17, 1), nullable=True)
  fecha = Column(Date, nullable=True)
  comentario = Column(String(255), nullable=True)
  idcaja = Column(String(45), nullable=True)
  referencia = Column(String(45), nullable=True)
  tipo_documento = Column(
      Integer, ForeignKey("tipos_documento.id"), nullable=True
  )

  # Relaciones
  cliente = relationship("Cliente", back_populates="movimientos")
  factura = relationship("HFactura", back_populates="movimientos")
  tipo_doc_rel = relationship("TipoDocumento", back_populates="movimientos")