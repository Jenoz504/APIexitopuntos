from database import Base
from sqlalchemy import Column, Date, DateTime, Decimal, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship

class TipoDocumento(Base):
  __tablename__ = "tipos_documento"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(50), nullable=False)
  descripcion = Column(String(150), nullable=True)

  # Relación con movimientos
  movimientos = relationship("Movimiento", back_populates="tipo_doc_rel")