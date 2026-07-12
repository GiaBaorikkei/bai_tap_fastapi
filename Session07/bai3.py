"""
1. Phân tích I/O

Input (Request Body)

{
    "product_id": 101,
    "quantity": 2
}

Thành công

Điều kiện:
product_id tồn tại.
quantity > 0.
quantity <= stock.
Kết quả:
Trừ số lượng tồn kho.
Tạo đơn hàng mới.
Trả về HTTP 201 Created.

Ví dụ:

{
    "message": "Tạo đơn hàng thành công",
    "data": {
        "id": 1,
        "product_id": 101,
        "quantity": 2,
        "total": 2400000
    }
}

Thất bại

product_id không tồn tại
404 Not Found
{
    "detail": "Không tìm thấy sản phẩm"
}
quantity <= 0
400 Bad Request
{
    "detail": "Số lượng mua phải lớn hơn 0"
}
quantity > stock
400 Bad Request
{
    "detail": "Sản phẩm không đủ số lượng trong kho"
}
2. Các bước xử lý
Nhận product_id và quantity.
Tìm sản phẩm trong products_db.
Nếu không tìm thấy → raise HTTPException(404).
Nếu quantity <= 0 → raise HTTPException(400).
Nếu quantity > stock → raise HTTPException(400).
Trừ số lượng tồn kho.
Tạo đơn hàng mới.
Thêm đơn hàng vào orders_db.
Trả về 201 Created.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]

orders_db = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):

    # Kiểm tra sản phẩm
    product = next(
        (p for p in products_db if p["id"] == order.product_id),
        None
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )

    # Kiểm tra số lượng tồn kho
    if order.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    # Trừ kho
    product["stock"] -= order.quantity

    # Tạo đơn hàng
    new_order = {
        "id": len(orders_db) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total": order.quantity * product["price"]
    }

    orders_db.append(new_order)

    return {
        "message": "Tạo đơn hàng thành công",
        "data": new_order
    }