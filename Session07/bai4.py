"""
1. Phân tích Input/Output

Input

Endpoint: GET /orders/{order_id}/payment
Path Parameter:
order_id: int

Output

Thành công (200 OK)

{
    "payment_status": "PAID",
    "method": "BANK_TRANSFER"
}

Không tìm thấy đơn hàng (404 Not Found)

{
    "detail": "Không tìm thấy đơn hàng"
}

Lỗi hệ thống (500 Internal Server Error)

{
    "detail": "Đã xảy ra lỗi hệ thống"
}
Giải pháp 1: Lưu dữ liệu bằng List
orders_list = [
    {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
]

Tra cứu:

order = next((o for o in orders_list if o["id"] == order_id), None)
Phải duyệt từng phần tử.
Độ phức tạp O(n).
Giải pháp 2: Lưu dữ liệu bằng Dict
orders_db = {
    1: {
        "code": "SP001",
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "code": "SP002",
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}

Tra cứu:

order = orders_db.get(order_id)
Tra cứu trực tiếp theo key.
Độ phức tạp trung bình O(1).
Phần 2. So sánh & Lựa chọn
Tiêu chí	                Giải pháp 1: Duyệt List	            Giải pháp 2: Dùng Dict
Tốc độ tìm kiếm	            Chậm, O(n)	                        Nhanh, O(1)
Bộ nhớ tiêu hao	            Ít hơn	                            Cao hơn một chút do lưu key
Độ dễ hiểu	                Đơn giản	                        Dễ hiểu
Khả năng bảo trì	        Khó mở rộng khi dữ liệu lớn	        Dễ mở rộng và bảo trì
Bối cảnh phù hợp	        Dữ liệu nhỏ	                        Dữ liệu lớn, tra cứu nhiều
"""
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

orders_db = {
    1: {
        "code": "SP001",
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "code": "SP002",
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}

@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):
    try:
        order = orders_db.get(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy đơn hàng"
            )

        return {
            "payment_status": order["payment_status"],
            "method": order["method"]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống"
        )