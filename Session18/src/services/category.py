from src.models.category import Category
from src.schema.category import CreateCategory

def get_category(db):
    category = db.query(Category).all()
    return {
        "message": "Lấy tất cả danh mục",
        "data": category
    }
def create_category(category:CreateCategory, db):
    new_category = Category (
        name = category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {
        "message": "Thêm danh mục thành công.",
        "data": new_category
    }