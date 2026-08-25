from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# 1. FIX: Cấu hình CORS chỉ cho phép 2 frontend cụ thể
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}

# 2. FIX: Cập nhật Middleware bỏ qua OPTIONS và API public
@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    # Đã thêm "/login" vào danh sách API công khai để không bị lỗi 401 khi đăng nhập
    public_paths = ["/health", "/docs", "/openapi.json", "/redoc", "/login"]

    # Bỏ qua kiểm tra auth nếu là preflight request hoặc API công khai
    if request.method == "OPTIONS" or request.url.path in public_paths:
        response = await call_next(request)
    else:
        # Xử lý kiểm tra auth cho các API bảo vệ
        if "authorization" not in request.headers:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header is required"},
            )
        response = await call_next(request)

    # Thêm custom header cho toàn bộ response
    response.headers["X-System-Name"] = "Learning Management System"
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = TOKENS.get(token)

    # Token không hợp lệ
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
        
    # FIX: Chặn những tài khoản đang bị khóa (is_active = False)
    if not user.get("is_active"):
        raise HTTPException(
            status_code=403,
            detail="User account is locked/inactive",
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)):
    # 3. FIX: Sửa điều kiện phân quyền (Chỉ admin mới được đi tiếp)
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required",
        )

    return current_user


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/courses")
def get_courses(current_user: dict = Depends(get_current_user)):
    return {
        "items": [
            {"id": 1, "name": "FastAPI Basic"},
            {"id": 2, "name": "FastAPI Security"},
        ]
    }


@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }
    
# Thêm API xử lý đăng nhập
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Cấp token giả lập tương ứng với username
    if form_data.username == "admin01":
        return {"access_token": "admin-token", "token_type": "bearer"}
    
    if form_data.username == "student01":
        return {"access_token": "user-token", "token_type": "bearer"}
        
    if form_data.username == "locked01":
        return {"access_token": "locked-token", "token_type": "bearer"}

    # Báo lỗi nếu nhập sai
    raise HTTPException(
        status_code=400, 
        detail="Incorrect username or password"
    )