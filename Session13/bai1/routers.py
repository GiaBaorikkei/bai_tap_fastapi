from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from services import *

router = APIRouter()


def response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.post("/menu-items")
def create_menu(
        request: Request,
        item: MenuItemCreate,
        db: Session = Depends(get_db)
):
    menu = create_menu_item(db, item)

    return response(
        200,
        "Thêm món ăn thành công",
        None,
        MenuItemResponse.model_validate(menu).model_dump(),
        request.url.path
    )


@router.get("/menu-items")
def get_all_menu(
        request: Request,
        db: Session = Depends(get_db)
):
    data = [
        MenuItemResponse.model_validate(i).model_dump()
        for i in get_all_menu_items(db)
    ]

    return response(
        200,
        "Lấy danh sách món ăn thành công",
        None,
        data,
        request.url.path
    )


@router.get("/menu-items/{item_id}")
def get_menu(
        item_id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    menu = get_menu_item(db, item_id)

    return response(
        200,
        "Lấy món ăn thành công",
        None,
        MenuItemResponse.model_validate(menu).model_dump(),
        request.url.path
    )


@router.put("/menu-items/{item_id}")
def update_menu(
        item_id: int,
        item: MenuItemUpdate,
        request: Request,
        db: Session = Depends(get_db)
):
    menu = update_menu_item(db, item_id, item)

    return response(
        200,
        "Cập nhật món ăn thành công",
        None,
        MenuItemResponse.model_validate(menu).model_dump(),
        request.url.path
    )


@router.delete("/menu-items/{item_id}")
def delete_menu(
        item_id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    delete_menu_item(db, item_id)

    return response(
        200,
        "Xóa món ăn thành công",
        None,
        None,
        request.url.path
    )