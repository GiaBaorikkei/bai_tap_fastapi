from pydantic import BaseModel


#  VALIDATE DỮ LIỆU TỪ CLIENT GỬI LÊN VÀ CẤU HÌNH RESPONSE TRẢ VỀ

class ProductCreate(BaseModel):
    name: str
    price: float