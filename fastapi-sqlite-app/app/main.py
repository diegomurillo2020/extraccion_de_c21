from fastapi import FastAPI
from .database import engine
from . import models
from .routers import registro # 🆕 Importar el nuevo router

# 1. Crear las tablas (incluida RegistroContable)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Registros Contables")

# 2. Incluir Routers
app.include_router(registro.router)

# 3. Ruta Raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API lista. Explora /docs para ver los endpoints de Registros Contables."}