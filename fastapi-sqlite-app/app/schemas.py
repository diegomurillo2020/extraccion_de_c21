from pydantic import BaseModel

# 1. Esquema Base: Propiedades comunes para creación y lectura
class ItemBase(BaseModel):
    title: str
    description: str | None = None

# 2. Esquema de Creación: Usado para validar la data que llega por POST
class ItemCreate(ItemBase):
    pass

# 3. Esquema de Respuesta: Usado para serializar la data que sale de la API (incluye el ID)
class Item(ItemBase):
    id: int

    class Config:
        # Permite que Pydantic lea la data como un objeto ORM de SQLAlchemy
        from_attributes = True

class UserBase(BaseModel):
    email: str
    is_active: bool | None = True

# Esquema para crear un User (requiere password)
class UserCreate(UserBase):
    password: str

# Esquema de Respuesta para User (nunca devolvemos el password)
class User(UserBase):
    id: int

    class Config:
        from_attributes = True