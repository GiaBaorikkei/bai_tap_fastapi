"""
Phần 1: Phân tích & Đề xuất đa giải pháp
1. Phân tích Input / Output
Input

API PUT /products/{product_id} nhận:

Path Parameter: product_id
Request Body:
code
name
price
stock
Output

Thành công:

Cập nhật sản phẩm thành công.
Trả về thông tin sản phẩm sau khi cập nhật.

Thất bại:

Không tìm thấy sản phẩm.
Mã sản phẩm bị trùng.
Dữ liệu không hợp lệ (tên rỗng, giá ≤ 0, tồn kho < 0).
2. Đề xuất 2 giải pháp
Giải pháp 1: Duyệt list
Dùng vòng lặp for tìm sản phẩm theo id.
Kiểm tra code có bị trùng với sản phẩm khác không.
Nếu hợp lệ thì cập nhật dữ liệu.

Ưu điểm: Dễ hiểu, phù hợp dữ liệu nhỏ.

Nhược điểm: Tìm kiếm chậm khi dữ liệu lớn.

Giải pháp 2: Dùng dict
Chuyển danh sách sản phẩm thành dict với id là key.
Tìm kiếm theo id nhanh hơn.
Sau đó kiểm tra code và cập nhật.

Ưu điểm: Tìm kiếm nhanh.

Nhược điểm: Tốn thêm bộ nhớ và code phức tạp hơn.

Phần 2: So sánh & Lựa chọn
Tiêu chí	        Giải pháp 1: Duyệt list	        Giải pháp 2: Dùng dict
Tốc độ tìm kiếm	    Chậm	                        Nhanh
Bộ nhớ	            Ít	                            Nhiều hơn
Dễ hiểu	            Dễ	                            Trung bình
Dễ bảo trì	        Dễ	                            Khá tốt
Bối cảnh phù hợp	Dữ liệu nhỏ	                    Dữ liệu lớn
Kết luận

Em chọn Giải pháp 1 (duyệt list) vì bài toán có dữ liệu ít, cách làm đơn giản và phù hợp với kiến thức đã học.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]


class ProductUpdate(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    # Kiểm tra sản phẩm tồn tại
    product_found = None
    for p in products:
        if p["id"] == product_id:
            product_found = p
            break

    if product_found is None:
        return {
            "detail": "Product not found"
        }

    # Kiểm tra trùng mã sản phẩm
    for p in products:
        if p["code"] == product.code and p["id"] != product_id:
            return {
                "detail": "Product code already exists"
            }

    # Cập nhật thông tin
    product_found["code"] = product.code
    product_found["name"] = product.name
    product_found["price"] = product.price
    product_found["stock"] = product.stock

    return {
        "message": "Update product successfully",
        "data": product_found
    }