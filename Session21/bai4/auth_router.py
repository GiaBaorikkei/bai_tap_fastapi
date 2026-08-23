from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database import get_db
from user import User

from auth import (
    RegisterRequest,
    LoginRequest,
    LoginResponse
)

from security import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Kiểm tra email đã tồn tại
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    # Băm password
    password_hash = hash_password(
        data.password
    )

    # Tạo user
    new_user = User(
        email=data.email,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Đăng ký thành công",
        "data": {
            "id": new_user.id,
            "email": new_user.email
        }
    }


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Tìm user
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # Không tìm thấy user
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # Kiểm tra password
    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # Tạo JWT
    access_token = create_access_token(
        user.id,
        user.email
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }