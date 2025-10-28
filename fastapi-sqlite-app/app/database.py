from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Define dónde se guardará el archivo SQLite
DATABASE_URL = "sqlite:///./app.db"

# create_engine: Se conecta a la BD. El argumento 'check_same_thread=False' es necesario para SQLite en FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: Fábrica de sesiones para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Clase base para que los modelos de SQLAlchemy hereden
class Base(DeclarativeBase):
    pass

# Dependency: Inyector de dependencias para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()