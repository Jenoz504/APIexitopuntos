from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.cliente import Cliente, UsuarioApp
from passlib.context import CryptContext
from schemas.cliente_schema import (  # <-- Aquí está el cambio clave
    ClienteRegisterSchema,
    ClienteResponseSchema,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configuración de Bcrypt para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
  return pwd_context.hash(password)


@router.post(
    "/register",
    response_model=ClienteResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_client(data: ClienteRegisterSchema, db: Session = Depends(get_db)):
  # 1. Verificar si el DNI (idcliente) ya existe en la tabla de clientes de ExitoSystems
  cliente = (
      db.query(Cliente).filter(Cliente.idcliente == data.idcliente).first()
  )

  if not cliente:
    # Si no existe en la BD de la abarrotería, lo creamos automáticamente como cliente nuevo
    cliente = Cliente(
        idcliente=data.idcliente,
        nombre=data.nombre,
        telefono=data.telefono,
        cuenta=0.00,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
  else:
    # Si ya existe en caja pero se está registrando por primera vez en la app, actualizamos su nombre si es necesario
    if not cliente.telefono and data.telefono:
      cliente.telefono = data.telefono
      db.commit()

  # 2. Verificar si ya existe un usuario de app asociado a ese DNI o correo
  existing_user = (
      db.query(UsuarioApp)
      .filter(
          (UsuarioApp.idcliente == data.idcliente)
          | (UsuarioApp.email == data.email)
      )
      .first()
  )
  if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            "Ya existe una cuenta web registrada con este DNI o correo"
            " electrónico."
        ),
    )

  # 3. Crear el usuario de la app con la contraseña hasheada
  hashed_password = get_password_hash(data.password)
  nuevo_usuario_app = UsuarioApp(
      idcliente=cliente.idcliente,
      email=data.email,
      password_hash=hashed_password,
      auth_provider="local",
  )

  db.add(nuevo_usuario_app)
  db.commit()

  # Retornar datos del cliente
  return {
      "idcliente": cliente.idcliente,
      "nombre": cliente.nombre,
      "telefono": cliente.telefono,
      "email": nuevo_usuario_app.email,
      "cuenta": cliente.cuenta,
  }