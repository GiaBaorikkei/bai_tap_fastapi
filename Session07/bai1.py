"""
STT	Dữ liệu gửi lên	        Kết quả hiện tại (Mã HTTP + Body)	            Kết quả đúng mong muốn	               Lỗi phát hiện
1	GET /orders/999	        HTTP 200 OK                                     HTTP 404 Not Found                     Trả sai mã trạng thái HTTP. Không tìm thấy đơn hàng 
                            {"message":"Order not found"}	                {"message":"Order not found"}          nhưng vẫn trả về 200 OK thay vì 404 Not Found, vi 
                                                                            (hoặc thông báo tương tự)              phạm chuẩn RESTful API.
2	GET /orders/1	        HTTP 200 OK                                     HTTP 200 OK
                            {"id":1,"customer_name":"Nguyen Van             {"id":1,"customer_name":"Nguyen Van A  Lộ thông tin nhạy cảm. API trả về hai trường nội
                            A","total_amount":1500000.0,"profit_margin":0.25,""total_amount":1500000.0}              bộ profit_margin và supplier_id, vi phạm yêu cầu bảo mật.
                            "supplier_id":"SUP_DELL_01"}	
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,
        "supplier_id": "SUP_DELL_01"
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,
        "supplier_id": "SUP_LOGI_02"
    }
]

# Model trả về cho client (không chứa dữ liệu nhạy cảm)
class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )