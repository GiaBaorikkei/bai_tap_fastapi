from pydantic import BaseModel

class CreateProduct(BaseModel):
    product_name: str
    price: float
    category_id: int