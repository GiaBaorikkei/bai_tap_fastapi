from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)

from services import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item_by_id,
    update_menu_item,
    delete_menu_item
)


router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


def current_timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@router.post("")
def create_item(
    menu_item: MenuItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = create_menu_item(db, menu_item)

    if error == "DISH_CODE_EXISTS":
        return JSONResponse(
            status_code=400,
            content={
                "statusCode": 400,
                "message": "Dish code đã tồn tại",
                "error": "Bad Request",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    if error == "DATABASE_ERROR":
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "message": "Lỗi cơ sở dữ liệu",
                "error": "Internal Server Error",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    return {
        "statusCode": 201,
        "message": "Thêm món ăn thành công",
        "error": None,
        "data": MenuItemResponse.model_validate(item).model_dump(
            mode="json"
        ),
        "path": request.url.path,
        "timestamp": current_timestamp()
    }



@router.get("")
def get_items(
    request: Request,
    db: Session = Depends(get_db)
):
    items = get_all_menu_items(db)

    data = [
        MenuItemResponse.model_validate(item).model_dump(
            mode="json"
        )
        for item in items
    ]

    return {
        "statusCode": 200,
        "message": "Lấy danh sách món ăn thành công",
        "error": None,
        "data": data,
        "path": request.url.path,
        "timestamp": current_timestamp()
    }



@router.get("/{item_id}")
def get_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    item = get_menu_item_by_id(db, item_id)

    if not item:
        return JSONResponse(
            status_code=404,
            content={
                "statusCode": 404,
                "message": "Menu item not found",
                "error": "Not Found",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    return {
        "statusCode": 200,
        "message": "Lấy thông tin món ăn thành công",
        "error": None,
        "data": MenuItemResponse.model_validate(item).model_dump(
            mode="json"
        ),
        "path": request.url.path,
        "timestamp": current_timestamp()
    }


@router.put("/{item_id}")
def update_item(
    item_id: int,
    menu_item: MenuItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = update_menu_item(
        db,
        item_id,
        menu_item
    )

    if error == "NOT_FOUND":
        return JSONResponse(
            status_code=404,
            content={
                "statusCode": 404,
                "message": "Menu item not found",
                "error": "Not Found",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    if error == "DISH_CODE_EXISTS":
        return JSONResponse(
            status_code=400,
            content={
                "statusCode": 400,
                "message": "Dish code đã tồn tại",
                "error": "Bad Request",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    if error == "DATABASE_ERROR":
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "message": "Lỗi cơ sở dữ liệu",
                "error": "Internal Server Error",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    return {
        "statusCode": 200,
        "message": "Cập nhật món ăn thành công",
        "error": None,
        "data": MenuItemResponse.model_validate(item).model_dump(
            mode="json"
        ),
        "path": request.url.path,
        "timestamp": current_timestamp()
    }



@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    success, error = delete_menu_item(
        db,
        item_id
    )

    if error == "NOT_FOUND":
        return JSONResponse(
            status_code=404,
            content={
                "statusCode": 404,
                "message": "Menu item not found",
                "error": "Not Found",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    if error == "DATABASE_ERROR":
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "message": "Lỗi cơ sở dữ liệu",
                "error": "Internal Server Error",
                "data": None,
                "path": request.url.path,
                "timestamp": current_timestamp()
            }
        )

    return {
        "statusCode": 200,
        "message": "Xóa món ăn thành công",
        "error": None,
        "data": None,
        "path": request.url.path,
        "timestamp": current_timestamp()
    }