"""
Luồng xử lý của hệ thống

Client gửi request DELETE /orders/{order_id}.
FastAPI kiểm tra dữ liệu đầu vào.
Nếu sai kiểu dữ liệu (order_id không phải số) → RequestValidationError.
API xử lý nghiệp vụ:
Không tìm thấy đơn hàng → HTTPException(404).
Đơn hàng đã DELIVERED → HTTPException(400).
Đơn hàng PENDING → cập nhật trạng thái thành CANCELLED.
Nếu phát sinh lỗi ngoài dự kiến (Runtime Error) → Exception.
Các lỗi đều được Global Exception Handler bắt lại và trả về cùng một cấu trúc JSON gồm 6 trường:
{
    "statusCode": 400,
    "message": "...",
    "data": null,
    "error": "...",
    "timestamp": "...",
    "path": "..."
}
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI()

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"}
]

# ==========================
# Global Exception Handlers
# ==========================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "statusCode": 422,
            "message": "Dữ liệu không hợp lệ",
            "data": None,
            "error": exc.errors(),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.detail,
            "data": None,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "statusCode": 500,
            "message": "Đã xảy ra lỗi hệ thống",
            "data": None,
            "error": "Internal Server Error",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

# ==========================
# API Hủy đơn hàng
# ==========================

@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):

    order = next((o for o in orders_db if o["id"] == order_id), None)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng"
        )

    if order["status"] == "DELIVERED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể hủy đơn hàng đã giao"
        )

    order["status"] = "CANCELLED"

    return {
        "statusCode": 200,
        "message": "Hủy đơn hàng thành công",
        "data": order,
        "error": None,
        "timestamp": datetime.now().isoformat(),
        "path": f"/orders/{order_id}"
    }