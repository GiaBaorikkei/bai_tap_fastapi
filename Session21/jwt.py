"""
JWT: json web token 

ĐĂNG KÝ:
"""

user ={
    "email": "bao@gmail.com",
    "name": "Bảo",
    "password": "123456",
    "address": "HN",
    "sdt": "123456789",
    "role": "user"
}

# Sau khi đăng ký thành công
user ={
    "email": "bao@gmail.com",
    "name": "Bảo",
    "password": "abcxyz",
    "address": "HN",
    "sdt": "123456789",
    "role": "user"
}
# khi tiến hành đăng nhập thì server sẽ tạo ra các JWT trả về cho client lưu lại
# Mỗi lần lient truy cập API (request) thì sẽ biết ông đấy là ai, có quyền gì?
"""
    JWT gồm bao nhiêu phần: 3 phần
    phần 1: header _ phần đầu   : Thông tin thuật toán mã hoá
    phần 2: payload _ nội dung  : Thông tin người dùng
        {
            "user_id": 1,
            "name": "Bảo",
            "role": "user"
        }
    phần 3: signature _ chữ kí  : Đánh dấu người dùng
    
    khi tạo token (iwt) tạo sao người ta hay set time cho nó?
"""