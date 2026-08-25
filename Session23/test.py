"""
khi 1 user muốn gọi API mà server muốn biết ai là người gọi API đấy, có bao nhiêu cách?
/users/profile -- hiện trang cá nhân của Đạt.
C!: khi người dùng đăng nhập thành công thì lưu user_id và client, mỗi request + user_id
VẤN ĐỀ: dễ bị giả mạo
localstorage.setItem("user_id", 1)
C2: dùng JWT
    + Đăng nhập thành công
    + Server sẽ tạo ta JWT --> trả về client lưu lại
    + Mỗi lần gọi API + JWT
    + Thành phần JWT:
    p1. header _ thông tin thuật toán
    p2. payload (user_id:1, role:user)
    p3: signature ( chữ ký)
    Nếu bị lộ JWT: Thì người khác sẽ truy cập
"""