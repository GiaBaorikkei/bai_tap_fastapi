from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas import *
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


@router.post("/boarding-slots")
def create(
        request: Request,
        slot: BoardingSlotCreate,
        db: Session = Depends(get_db)
):

    slot = create_slot(db, slot)

    return response(
        200,
        "Thêm khoang lưu trú thành công",
        None,
        BoardingSlotResponse.model_validate(slot).model_dump(),
        request.url.path
    )


@router.get("/boarding-slots")
def get_all(
        request: Request,
        db: Session = Depends(get_db)
):

    data = [
        BoardingSlotResponse.model_validate(i).model_dump()
        for i in get_all_slots(db)
    ]

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        request.url.path
    )


@router.get("/boarding-slots/{slot_id}")
def get_one(
        slot_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    slot = get_slot(db, slot_id)

    return response(
        200,
        "Lấy khoang lưu trú thành công",
        None,
        BoardingSlotResponse.model_validate(slot).model_dump(),
        request.url.path
    )


@router.put("/boarding-slots/{slot_id}")
def update(
        slot_id: int,
        slot: BoardingSlotUpdate,
        request: Request,
        db: Session = Depends(get_db)
):

    slot = update_slot(db, slot_id, slot)

    return response(
        200,
        "Cập nhật khoang lưu trú thành công",
        None,
        BoardingSlotResponse.model_validate(slot).model_dump(),
        request.url.path
    )


@router.delete("/boarding-slots/{slot_id}")
def delete(
        slot_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    delete_slot(db, slot_id)

    return response(
        200,
        "Xóa khoang lưu trú thành công",
        None,
        None,
        request.url.path
    )