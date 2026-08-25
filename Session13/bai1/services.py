from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate


def create_menu_item(
    db: Session,
    menu_item: MenuItemCreate
):
    try:
        # Kiểm tra dish_code đã tồn tại chưa
        existing_item = (
            db.query(MenuItem)
            .filter(MenuItem.dish_code == menu_item.dish_code)
            .first()
        )

        if existing_item:
            return None, "DISH_CODE_EXISTS"

        new_item = MenuItem(
            dish_code=menu_item.dish_code,
            dish_name=menu_item.dish_name,
            calorie_count=menu_item.calorie_count,
            price=menu_item.price,
            status=menu_item.status.value
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item, None

    except IntegrityError:
        db.rollback()
        return None, "DISH_CODE_EXISTS"

    except SQLAlchemyError:
        db.rollback()
        return None, "DATABASE_ERROR"


def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()



def get_menu_item_by_id(
    db: Session,
    item_id: int
):
    return (
        db.query(MenuItem)
        .filter(MenuItem.id == item_id)
        .first()
    )



def update_menu_item(
    db: Session,
    item_id: int,
    menu_item: MenuItemUpdate
):
    try:
        item = get_menu_item_by_id(db, item_id)

        if not item:
            return None, "NOT_FOUND"

        # Lấy những trường thực sự được truyền lên
        update_data = menu_item.model_dump(
            exclude_unset=True
        )

        # Nếu cập nhật dish_code thì kiểm tra trùng
        if "dish_code" in update_data:
            existing_item = (
                db.query(MenuItem)
                .filter(
                    MenuItem.dish_code == update_data["dish_code"],
                    MenuItem.id != item_id
                )
                .first()
            )

            if existing_item:
                return None, "DISH_CODE_EXISTS"

        # Ghi đè trực tiếp thuộc tính Model
        for key, value in update_data.items():

            if key == "status":
                value = value.value

            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item, None

    except IntegrityError:
        db.rollback()
        return None, "DISH_CODE_EXISTS"

    except SQLAlchemyError:
        db.rollback()
        return None, "DATABASE_ERROR"



def delete_menu_item(
    db: Session,
    item_id: int
):
    try:
        item = get_menu_item_by_id(db, item_id)

        if not item:
            return False, "NOT_FOUND"

        db.delete(item)
        db.commit()

        return True, None

    except SQLAlchemyError:
        db.rollback()
        return False, "DATABASE_ERROR"