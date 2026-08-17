from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate


def create_menu_item(db: Session, item: MenuItemCreate):

    exist = db.query(MenuItem).filter(
        MenuItem.dish_code == item.dish_code
    ).first()

    if exist:
        raise HTTPException(400, "Dish code already exists")

    try:
        new_item = MenuItem(**item.model_dump())

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item

    except Exception:
        db.rollback()
        raise


def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()


def get_menu_item(db: Session, item_id: int):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(404, "Menu item not found")

    return item


def update_menu_item(db: Session, item_id: int, menu: MenuItemUpdate):

    item = get_menu_item(db, item_id)

    if menu.dish_code:

        exist = db.query(MenuItem).filter(
            MenuItem.dish_code == menu.dish_code,
            MenuItem.id != item_id
        ).first()

        if exist:
            raise HTTPException(400, "Dish code already exists")

    try:

        data = menu.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item

    except Exception:
        db.rollback()
        raise


def delete_menu_item(db: Session, item_id: int):

    item = get_menu_item(db, item_id)

    try:
        db.delete(item)
        db.commit()

    except Exception:
        db.rollback()
        raise