"""
Phần 1: Luồng dữ liệu

Khi client gửi request PATCH /products/{product_id}, hệ thống sẽ xử lý theo các bước:

Nhận product_id từ Path Parameter.
Tìm sản phẩm theo product_id.
Nếu không tìm thấy, trả về "Product not found".
Nếu sản phẩm đã có is_active = False, trả về "Product already inactive".
Nếu sản phẩm đang hoạt động (is_active = True), cập nhật is_active = False.
Trả về thông báo ngừng kinh doanh thành công cùng thông tin sản phẩm.
"""

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False}
]


@app.patch("/products/{product_id}")
def inactive_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            if product["is_active"] == False:
                return {
                    "message": "Product already inactive"
                }

            product["is_active"] = False

            return {
                "message": "Product inactive successfully",
                "data": product
            }

    return {
        "message": "Product not found"
    }