from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from user import User
from auth import RegisterRequest, LoginRequest

from security import (
    validate_password,
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


def register_user(
    user_data: RegisterRequest,
    db: Session
):

    # Kiểm tra email đã tồn tại
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được đăng ký"
        )

    # Kiểm tra password
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Mật khẩu phải có ít nhất 8 ký tự, "
                "bao gồm chữ hoa, chữ thường và chữ số"
            )
        )

    # Hash password
    password_hash = hash_password(
        user_data.password
    )

    # Tạo user
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
        role="student",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    login_data: LoginRequest,
    db: Session
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    # Không nói rõ email hay password sai
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # Kiểm tra tài khoản bị khóa
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản đã bị khóa"
        )

    # Kiểm tra password
    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # Tạo JWT
    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }