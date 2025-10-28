from fastapi import FastAPI
from . import models
from .database import engine
from .routers import items  # 🆕 Router de Items
from .routers import users  # Router de Users (asumiendo que lo creaste)

# 1. Crear las tablas al iniciar la app (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Aplicación FastAPI Modular") # Opcional: añade título

# 2. Incluir Routers
app.include_router(items.router)
app.include_router(users.router) # Si no existe, puedes comentarla por ahora

# 3. Ruta Raíz única
@app.get("/", tags=["Root"])
def read_root():
    """Endpoint de bienvenida."""
    return {"message": "¡Bienvenido! API en arquitectura modular con Items y Users"}