from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.services.product import get_product, create_product, get_product_detail
from src.schema.product import CreateProduct

router_product = APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router_product.get("/")
def get_all_product(db:Session = Depends(get_db)):
    return get_product(db)

@router_product.post("")
def add_product(product:CreateProduct, db: Session= Depends(get_db)):
    return create_product(product,db)

@router_product.get("{product_id}")
def get_product_by_id(product_id: int, db: Session=Depends(get_db)):
    return get_product_detail(product_id, db)