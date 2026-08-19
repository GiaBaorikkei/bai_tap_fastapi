from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.services.category import get_category, create_category
from src.schema.category import CreateCategory

router_category = APIRouter(
    prefix="/category",
    tags=["Category"]
)

@router_category.get("")
def get_all_category(db:Session = Depends(get_db)):
    return get_category(db)

@router_category.post("")
def add_category(category:CreateCategory, db: Session= Depends(get_db)):
    return create_category(category,db)