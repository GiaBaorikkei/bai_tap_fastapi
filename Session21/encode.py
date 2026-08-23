"""

MÃ HOÁ MẬT KHẨU:
1. Tại sao cần mã hoá
2. Khi nào tiến hành mã hoá
3. Mã hoá như thế nào

Khi đăng ký tài khoản: Hệ thống dùng các kỹ thuật(bycypt) để mã hoá(hash) mật khẩu để lưu vào database
12345 ==> abcxyz
12345 ==> klmnpq

abcxyz: gồm 4 phần
    1. Tên kỹ thuật mã hoá
    2. cost (chi phí mã hoá)
    3. muối (salt)
    4. mã hoá (chuỗi mật khẩu được mã hoá)
khi đăng nhập tài khoản:
    B1: Nhập tài khoản và mật khẩu
    B2: Hệ thống kiểm tra tên tài khoản có đúng hay không
        + Nếu sai hiển thị thông báo: tên tk hoặc mk không đúng
        + nếu đúng lấy ra mật khẩu đã được mã hoá
    B3: từ chuỗi mật khẩu đã được mã hoá lấy ra muối (salt) + pass mật khẩu sau đó verify mật khẩu
    
MÃ HOÁ 1 CHIỀU.
CÁC HACKER MUỐN HACK MẬT KHẨU THÌ ĐẦU TIÊN PHẢI CÓ ĐƯỢC CHUỖI MÃ HOÁ TRONG DB SAU ĐÓ TẠO RA CÁC MK NGƯỜI DÙNG HAY DÙNG
VD: 123456, admin, admin@@, ...
kết hợp với salt + để verify với chuỗi mã hoá

"""

import bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    )
    
    return hashed_password.decode("utf-8")
print("mk3", hash_password("12345"))
# mk1 $2b$12$Nfqeug14x/4JMNRvmNGK5.vUTQpp2W0XAsuXWtTNtfk3IUH7ahTua
"""
    1. tên kỹ thuật : $2b
    2. chi phí      : $12
    3. muối (salt)  : $Nfqeug14x/4JMNRvmNGK5
    4. mật khẩu sau khi mã hoá: vUTQpp2W0XAsuXWtTNtfk3IUH7ahTua
"""
# mk2 $2b$12$XNrXk0uQgBgVC96gxP9jnuebuVgYAN9wwy4afQdMAMEMMqwUFRddS
# mk3 $2b$12$W3PgYKcx15jD3qu7CPjZyuVUkq4tNUgsAOnZy47wqxTy9956g3mGC


# đăng nhập
#type hints
def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
print(verify_password("12345", "$2b$12$Nfqeug14x/4JMNRvmNGK5.vUTQpp2W0XAsuXWtTNtfk3IUH7ahTua"))