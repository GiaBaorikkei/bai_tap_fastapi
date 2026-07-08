"""
1. Input của bài toán
API nhận hai Query Parameters:
keyword
max_price

2. Output mong muốn
Nếu không truyền Query Parameter nào, trả về toàn bộ danh sách sản phẩm.
Nếu truyền keyword, trả về các sản phẩm có tên chứa từ khóa (
Nếu truyền max_price, trả về các sản phẩm có giá nhỏ hơn hoặc bằng max_price.
Nếu truyền cả keyword và max_price, chỉ trả về các sản phẩm thỏa mãn cả hai điều kiện.
Nếu max_price < 0, trả về thông báo lỗi:
{
    "detail": "max_price không được âm"
}

3. Đề xuất giải pháp xử lý bài toán
Khởi tạo danh sách products.
Tạo API GET /products.
Khai báo hai Query Parameters:
keyword: str
max_price: float
Kiểm tra nếu max_price < 0 thì trả về lỗi.
Duyệt qua danh sách sản phẩm.
Kiểm tra từng điều kiện:
Nếu có keyword, kiểm tra tên sản phẩm có chứa từ khóa hay không 
Nếu có max_price, kiểm tra giá sản phẩm có nhỏ hơn hoặc bằng giá tối đa hay không.
Những sản phẩm thỏa mãn điều kiện sẽ được đưa vào danh sách kết quả.
Trả về danh sách kết quả.

4. Thiết kế các bước xử lý

Bước 1: Khởi tạo ứng dụng FastAPI.
Bước 2: Khởi tạo danh sách products.
Bước 3: Tạo API GET /products.
Bước 4: Nhận keyword và max_price từ Query Parameters.
Bước 5: Kiểm tra max_price có âm hay không.
Bước 6: Duyệt từng sản phẩm trong danh sách.
Bước 7: Kiểm tra điều kiện tìm kiếm theo tên.
Bước 8: Kiểm tra điều kiện lọc theo giá.
Bước 9: Thêm sản phẩm hợp lệ vào danh sách kết quả.
Bước 10: Trả về danh sách kết quả.
"""

from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):

    if max_price is not None and max_price < 0:
        return {
            "detail": "max_price không được âm"
        }

    result = []

    for product in products:

        if keyword is not None:
            if keyword.lower() not in product["name"].lower():
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        result.append(product)

    return result