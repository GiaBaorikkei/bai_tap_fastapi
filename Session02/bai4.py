"""
Phần 1: Phân tích Input/Output

1. Input của bài toán là gì?

Danh sách books, mỗi sách gồm các thông tin: id, title, quantity.

2. Output mong muốn là gì?

API trả về danh sách các sách có quantity <= 5.
Nếu không có sách nào sắp hết hàng thì trả về:
{
    "message": "Không có sách nào sắp hết hàng",
    "data": []
}

3. Điều kiện để xác định sách sắp hết hàng là gì?

Sách có quantity <= 5.
Bỏ qua sách thiếu trường quantity.
Bỏ qua sách có quantity < 0.
Phần 2: Đề xuất giải pháp

Giải pháp 1: Dùng vòng lặp for

Duyệt từng sách trong danh sách.
Kiểm tra dữ liệu hợp lệ.
Nếu quantity <= 5 thì thêm vào danh sách kết quả.

Giải pháp 2: Dùng List Comprehension

Lọc danh sách bằng một biểu thức ngắn gọn.
Kết hợp điều kiện kiểm tra quantity và quantity <= 5.
Phần 3: So sánh và lựa chọn giải pháp

Tiêu chí	            Vòng lặp for	List comprehension
Độ dễ hiểu	            Cao	            Khá cao
Độ ngắn gọn	            Trung bình	    Cao
Dễ xử lý bẫy dữ liệu	Cao	            Trung bình
Dễ bảo trì	            Cao	            Khá cao

Giải pháp chọn: Vòng lặp for.

Lý do: Dễ đọc, dễ kiểm tra từng điều kiện và thuận tiện xử lý các trường hợp dữ liệu không hợp lệ như thiếu quantity hoặc quantity âm.

Phần 4: Thiết kế các bước xử lý
Khởi tạo ứng dụng FastAPI.
Khai báo danh sách books.
Tạo endpoint GET /books/low-stock.
Duyệt danh sách books.
Bỏ qua sách thiếu trường quantity.
Bỏ qua sách có quantity < 0.
Lấy các sách có quantity <= 5.
Nếu không có kết quả, trả về "Không có sách nào sắp hết hàng" và data là mảng rỗng.
Nếu có kết quả, trả về danh sách các sách sắp hết hàng.
"""

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20}
]

@app.get("/books/low-stock")
def get_low_stock_books():

    low_stock_books = []

    for book in books:

        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            low_stock_books.append(book)

    if len(low_stock_books) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }