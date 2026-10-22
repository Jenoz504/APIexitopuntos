from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship


class Cliente(Base):
  __tablename__ = "clientes"

  idcliente = Column(String(25), primary_key=True, index=True)
  nombre = Column(String(300), nullable=False)
  telefono = Column(String(15), nullable=True)
  cuenta = Column(Numeric(6, 2), nullable=True)

  # Relaciones
  movimientos = relationship("Movimiento", back_populates="cliente")
  usuario_app = relationship(
      "UsuarioApp", back_populates="cliente", uselist=False
  )


class UsuarioApp(Base):
  __tablename__ = "usuarios_app"

  id = Column(Integer, primary_key=True, autoincrement=True)
  idcliente = Column(
      String(25), ForeignKey("clientes.idcliente"), unique=True, nullable=False
  )
  email = Column(String(150), unique=True, index=True, nullable=True)
  password_hash = Column(String(255), nullable=True)
  auth_provider = Column(String(50), default="local")
  provider_id = Column(String(255), nullable=True)

  # Relaciones
  cliente = relationship("Cliente", back_populates="usuario_app")