from database import Base
from sqlalchemy import Column, Date, DateTime, Decimal, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship

class Inventario(Base):
  __tablename__ = "inventario"

  codigoProducto = Column(String(30), primary_key=True, index=True)
  producto = Column(String(45), nullable=True)
  precio = Column(Numeric(6, 2), nullable=True)
  existencias = Column(Numeric(17, 2), default=0.00)
  # Si deseas agregar un campo booleano para excluir productos de puntos, 
  # puedes añadirlo aquí o manejarlo a nivel de grupos de productos.