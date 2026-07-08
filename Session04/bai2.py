"""
1. Endpoint hiện tại có Path Parameter không?
Có.

2. Path Parameter trong bài này là gì?
Path Parameter là:
status

3. Khi gọi /orders/status/pending, biến status nhận giá trị gì?
Biến status sẽ nhận giá trị:
pending

4. Vì sao API hiện tại trả về sai dữ liệu?
Vì API không sử dụng giá trị status để lọc danh sách đơn hàng.
Mặc dù đã nhận được status từ URL, hàm lại trả về toàn bộ danh sách orders, nên kết quả bao gồm cả các đơn hàng có trạng thái paid và cancelled.

5. Dòng code nào đang khiến API bỏ qua giá trị status?
Dòng code:
return orders
Dòng này trả về toàn bộ danh sách đơn hàng mà không kiểm tra:
i["status"] == status
nên API không thực hiện đúng yêu cầu lọc theo trạng thái.
"""


from fastapi import FastAPI
app = FastAPI()
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    status_list = []
    for i in orders:
        if i["status"] == status:
            status_list.append(i)
    if len(status_list) > 0:
        return status_list
    
    return "Không tìm thấy trạng thái"