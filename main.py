from database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers de la aplicación
from routers import admin, auth, points

# Opcional: Esto crea automáticamente las tablas en MySQL si aún no existen
# (asegúrate de que los modelos estén importados si usas esto)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExitoPuntos API",
    version="1.0.0",
    description="Backend oficial de lealtad y puntos para ExitoSystems",
)

# Configuración de CORS (Permite que tu app web frontend consuma esta API sin bloqueos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes cambiar "*" por tu dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los Routers en la aplicación principal
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(points.router)


@app.get("/")
def read_root():
  return {
      "estado": "activo",
      "sistema": "ExitoPuntos API",
      "mensaje": "Servidor corriendo al 100% y listo para el frontend 🚀",
  }