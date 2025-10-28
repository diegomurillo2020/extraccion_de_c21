from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

# 🆕 Crea una instancia de APIRouter
router = APIRouter(
    prefix="/items",
    tags=["items"] # Agrupación en la documentación
)

@router.post("/", response_model=schemas.Item)
def create_item_route(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Crea un nuevo ítem en la base de datos."""
    return crud.create_item(db=db, item=item)

@router.get("/", response_model=list[schemas.Item])
def read_items_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los ítems."""
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=schemas.Item)
def read_item_route(item_id: int, db: Session = Depends(get_db)):
    """Obtiene un ítem por su ID."""
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return db_item

@router.delete("/{item_id}", response_model=schemas.Item)
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    """Elimina un ítem por su ID."""
    deleted_item = crud.delete_item(db, item_id=item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return deleted_item