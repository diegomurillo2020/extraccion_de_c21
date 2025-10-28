from sqlalchemy.orm import Session
# 🚨 Importar la función 'insert' y el dialecto de sqlite
from sqlalchemy.dialects.sqlite import insert 
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
# 🔄 FUNCIÓN DE CARGA MASIVA (BULK) CORREGIDA con Anti-Duplicados
# -----------------------------------------------------------

def bulk_create_registros(db: Session, df: pd.DataFrame):
    """
    Inserta múltiples registros en la BD desde un DataFrame de Pandas,
    ignorando silenciosamente los duplicados basados en (n_factura, rubro).
    """
    # 1. Renombrar las columnas del DataFrame a los nombres de snake_case del modelo
    df.columns = [
        "id", "usuario", "n_factura", "fecha_factura", "ref_bancaria", 
        "carnet", "nombres", "rubro", "cod_pago", "detalle", 
        "monto_total", "objeto", "volteos", "monto_siscom", 
        "monto_extracto", "diferencia_monto", "observacion"
    ]
    
    # 2. Convertir el DataFrame en una lista de diccionarios
    registros_data = df.to_dict('records')

    # 3. Definir la estrategia de inserción con manejo de conflictos
    # La clave de esto es usar la instrucción INSERT con on_conflict_do_nothing
    
    # Crea la sentencia INSERT con los valores
    stmt = insert(models.RegistroContable).values(registros_data)
    
    # 🚨 Añade la directiva de conflicto: IGNORAR DUPLICADOS 🚨
    # Esto usa la restricción UniqueConstraint definida en el modelo.
    stmt = stmt.on_conflict_do_nothing() 
    
    # 4. Ejecutar la inserción masiva
    try:
        # Ejecuta la sentencia que insertará solo las filas no duplicadas
        result = db.execute(stmt)
        db.commit()
        
        # En SQLite, el número de filas *realmente* insertadas es difícil de obtener
        # con DO NOTHING, por lo que retornamos el total de filas que se intentaron procesar.
        return len(registros_data)
        
    except Exception as e:
        db.rollback()
        # Relanzar el error para que sea manejado por el router
        raise e