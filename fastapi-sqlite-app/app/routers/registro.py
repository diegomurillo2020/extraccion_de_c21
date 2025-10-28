# app/routers/registro.py

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

# Importar Pandas e IO para manejo de archivos
import pandas as pd
import io

router = APIRouter(
    prefix="/registros",
    tags=["Registros Contables"]
)

# --- RUTAS CRUD EXISTENTES ---

@router.post("/", response_model=schemas.Registro)
def create_registro_route(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    """Crea un nuevo registro contable manualmente."""
    return crud.create_registro(db=db, registro=registro)

@router.get("/", response_model=list[schemas.Registro])
def read_registros_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los registros contables."""
    return crud.get_registros(db, skip=skip, limit=limit)

@router.get("/{registro_id}", response_model=schemas.Registro)
def read_registro_route(registro_id: int, db: Session = Depends(get_db)):
    """Obtiene un registro por su ID."""
    db_registro = crud.get_registro(db, registro_id=registro_id)
    if db_registro is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_registro

# --- ENDPOINT DE SUBIDA DE CSV (CORREGIDO) ---

@router.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Sube un archivo CSV y guarda los registros en la base de datos de forma masiva.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV.")

    try:
        # 1. Leer el archivo subido en memoria
        content = file.file.read()
        
        # 2. Convertir el contenido binario a un DataFrame de Pandas
        # 🚨 Usar 'latin-1' o 'Windows-1252' para evitar errores con caracteres especiales
        df = pd.read_csv(
            io.StringIO(content.decode('latin-1')),
            sep=';',
            header=0,
            usecols=range(17)
        )
        
        # 3. Llamar a la función CRUD para la inserción masiva
        registros_insertados = crud.bulk_create_registros(db, df)
        
        return {
            "status": "success",
            "filename": file.filename,
            "registros_insertados": registros_insertados,
            "message": f"Se han insertado {registros_insertados} registros contables exitosamente."
        }

    except Exception as e:
        # Esto te ayudará a depurar si hay errores de formato (e.g., texto en columna float)
        print(f"Error detallado: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo CSV. Revise el formato y las columnas: {e}"
        )
