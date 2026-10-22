from fastapi import FastAPI
from routers import auth  
app = FastAPI(
    title="ExitoPuntos API",
    version="1.0.0",
)

# Incluir las rutas de autenticación
app.include_router(auth.router)


@app.get("/")
def read_root():
  return {"message": "¡API de ExitoPuntos funcionando al 100%!"}