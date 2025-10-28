# app/models.py
from sqlalchemy import Column, Integer, String, Boolean # ⬅️ ¡Añadir Boolean aquí!
from .database import Base

# Clase que representa la tabla 'items'
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

# Clase que representa la tabla 'users'
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True) # ✅ Ahora 'Boolean' está definido.