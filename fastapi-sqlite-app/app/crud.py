# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

# 🆕 Importación de Pandas para el tipo DataFrame
import pandas as pd 

# --- Funciones CRUD para RegistroContable ---

def get_registro(db: Session, registro_id: int):
    return db.query(models.RegistroContable).filter(models.RegistroContable.id == registro_id).first()

def get_registros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RegistroContable).offset(skip).limit(limit).all()

def create_registro(db: Session, registro: schemas.RegistroCreate):
    db_registro = models.RegistroContable(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

# -----------------------------------------------------------
# 🆕 FUNCIÓN DE CARGA MASIVA (BULK) DESDE DATAFRAME
# -----------------------------------------------------------

def bulk_create_registros(db: Session, df: pd.DataFrame):
    """
    Inserta múltiples registros en la BD desde un DataFrame de Pandas.
    """
    # 1. Renombrar las columnas del DataFrame a los nombres de snake_case del modelo
    # Esto es crucial para que coincida con tu modelo de SQLAlchemy
    # NOTA: Los nombres de columna deben coincidir exactamente con los del CSV subido,
    # y deben estar en el orden esperado por este código.
    df.columns = [
        "id", "usuario", "n_factura", "fecha_factura", "ref_bancaria", 
        "carnet", "nombres", "rubro", "cod_pago", "detalle", 
        "monto_total", "objeto", "volteos", "monto_siscom", 
        "monto_extracto", "diferencia_monto", "observacion"
    ]
    
    # 2. Convertir el DataFrame en una lista de diccionarios
    # .to_dict('records') crea la lista de objetos que SQLAlchemy puede entender
    registros_data = df.to_dict('records')

    # 3. Crear los objetos modelo y añadirlos a la sesión
    # NOTA: Se usa .bulk_save_objects para una inserción eficiente
    db_registros = [models.RegistroContable(**data) for data in registros_data]
    
    db.bulk_save_objects(db_registros)
    db.commit()
    
    return len(db_registros)