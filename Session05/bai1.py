"""
Phần 1: Chỉ ra lỗi bằng test case
STT	Dữ liệu gửi lên	    Kết quả hiện tại	        Kết quả đúng mong muốn	            Lỗi phát hiện
1	code = "SP001"	    Vẫn tạo được sản phẩm mới	Báo lỗi mã sản phẩm đã tồn tại	    Không kiểm tra trùng mã sản phẩm
2	code = "SP002"	    Vẫn tạo được sản phẩm mới	Báo lỗi mã sản phẩm đã tồn tại	    Cho phép tạo sản phẩm có mã trùng

Kết luận: API chưa kiểm tra xem mã sản phẩm (code) đã tồn tại trong danh sách products hay chưa nên có thể tạo nhiều sản phẩm có cùng mã.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.post("/products")
def create_product(product: ProductCreate):

    for p in products:
        if p["code"] == product.code:
            return {
                "message": "Mã sản phẩm đã tồn tại"
            }

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }