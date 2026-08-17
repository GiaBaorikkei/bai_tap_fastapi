from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import BoardingSlot
from schemas import BoardingSlotCreate, BoardingSlotUpdate


def create_slot(db: Session, slot: BoardingSlotCreate):

    exist = db.query(BoardingSlot).filter(
        BoardingSlot.slot_number == slot.slot_number
    ).first()

    if exist:
        raise HTTPException(400, "Slot number already exists")

    try:
        new_slot = BoardingSlot(**slot.model_dump())

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return new_slot

    except Exception:
        db.rollback()
        raise


def get_all_slots(db: Session):
    return db.query(BoardingSlot).all()


def get_slot(db: Session, slot_id: int):

    slot = db.query(BoardingSlot).filter(
        BoardingSlot.id == slot_id
    ).first()

    if not slot:
        raise HTTPException(404, "Boarding slot not found")

    return slot


def update_slot(
    db: Session,
    slot_id: int,
    slot_update: BoardingSlotUpdate
):

    slot = get_slot(db, slot_id)

    if slot_update.slot_number:

        exist = db.query(BoardingSlot).filter(
            BoardingSlot.slot_number == slot_update.slot_number,
            BoardingSlot.id != slot_id
        ).first()

        if exist:
            raise HTTPException(400, "Slot number already exists")

    try:

        data = slot_update.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(slot, key, value)

        db.commit()
        db.refresh(slot)

        return slot

    except Exception:
        db.rollback()
        raise


def delete_slot(db: Session, slot_id: int):

    slot = get_slot(db, slot_id)

    try:
        db.delete(slot)
        db.commit()

    except Exception:
        db.rollback()
        raise