from sqlalchemy.orm import Session
from . import models, schemas

# 1. Función para obtener un item por ID
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# 2. Función para obtener todos los items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 3. Función para crear un item
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit() # Guardar los cambios
    db.refresh(db_item) # Actualizar el objeto con el ID generado
    return db_item

# 4. Función para eliminar un item (Opcional)
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None

# 🆕 Funciones CRUD de User

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # En un proyecto real, usarías bcrypt o argon2 para hashear el password.
    # Usamos un simple prefijo para simular el hasheo.
    fake_hashed_password = user.password + "notreallyhashed" 
    
    db_user = models.User(
        email=user.email, 
        hashed_password=fake_hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user