"""
| STT | Dữ liệu/Endpoint gửi lên | Kết quả hiện tại (Mã HTTP + Body) | Kết quả đúng mong muốn | Lỗi phát hiện |
|-----|---------------------------|-----------------------------------|------------------------|---------------|
| 1 | PUT /orders/999/status với {"status":"SHIPPING"} | HTTP 200 OK {"statusCode":200,"message":"Cập nhật thành công","data":null} | HTTP 404 Not Found {"detail":"Order not found"} | Không tìm thấy đơn hàng nhưng chỉ print() rồi vẫn trả về 200 OK, không dừng luồng xử lý. |
| 2 | PUT /orders/1/status với {"status":"TRONG_SANG"} | HTTP 200 OK {"error":"Trạng thái không hợp lệ"} | HTTP 400 Bad Request {"detail":"Trạng thái không hợp lệ"} | Trả lỗi bằng return thay vì raise HTTPException nên sai mã HTTP và không đúng chuẩn RESTful. |
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

# Loại bỏ Magic String
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"

class StatusUpdate(BaseModel):
    status: OrderStatus

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order["status"] = data.status.value

    return {
        "message": "Cập nhật thành công",
        "data": order
    }