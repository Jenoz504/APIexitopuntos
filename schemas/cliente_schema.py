from typing import Optional
from pydantic import BaseModel, EmailStr


# Esquema para registrar un cliente nuevo desde la App Web
class ClienteRegisterSchema(BaseModel):
  idcliente: str  # DNI del cliente (ej: 0501199912345)
  nombre: str  # Nombre completo
  telefono: Optional[str] = None  # Teléfono opcional
  email: EmailStr  # Correo electrónico para la app
  password: str  # Contraseña en texto plano (que será hasheada)


# Esquema para iniciar sesión
class ClienteLoginSchema(BaseModel):
  email: str
  password: str


# Esquema de respuesta al cliente (lo que devolvemos al frontend sin la contraseña)
class ClienteResponseSchema(BaseModel):
  idcliente: str
  nombre: str
  telefono: Optional[str] = None
  email: Optional[str] = None
  cuenta: Optional[float] = 0.00

  class Config:
    from_attributes = (
        True  # Permite leer modelos de SQLAlchemy directamente
    )