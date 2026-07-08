"""
1. Khi gọi GET /products/1, vì sao API trả về 404 Not Found?

Vì endpoint đang được khai báo là:
@app.get("/products/product_id")
FastAPI hiểu đây là đường dẫn cố định (/products/product_id), không phải đường dẫn có biến.

2. Dòng code nào đang khai báo sai Path Parameter?
@app.get("/products/product_id")

3. Vì sao /products/product_id không phải là Path Parameter?
Vì Path Parameter phải được đặt trong dấu {}.

4. Endpoint đúng cần sửa thành gì?
@app.get("/products/{product_id}")
"""

from fastapi import FastAPI
app = FastAPI()
products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {
        "message": "Không tìm thấy sản phẩm"
    }