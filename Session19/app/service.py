from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Warehouse, Package, Waybill
from app.schemas import WarehouseCreate, PackageUpdate


# ==========================================
# 1. TẠO NHÀ KHO
# ==========================================

def create_warehouse(
    data: WarehouseCreate,
    db: Session
):
    try:
        # Chuyển dữ liệu Pydantic sang dictionary
        warehouse_data = data.model_dump()

        # Tạo đối tượng Warehouse
        warehouse = Warehouse(
            **warehouse_data
        )

        # Thêm vào database
        db.add(warehouse)

        # Lưu thay đổi
        db.commit()

        # Lấy lại dữ liệu mới nhất
        db.refresh(warehouse)

        return warehouse

    except Exception:
        # Nếu xảy ra lỗi thì hủy transaction
        db.rollback()
        raise


# ==========================================
# 2. LẤY CHI TIẾT NHÀ KHO
# ==========================================

def get_warehouse_detail(
    warehouse_id: int,
    db: Session
):
    # Tìm Warehouse
    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

    # Không tìm thấy
    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Nhà kho không tồn tại"
        )

    # relationship packages sẽ tự lấy
    # danh sách Package liên quan
    return warehouse


# ==========================================
# 3. CẬP NHẬT PACKAGE
# ==========================================

def update_package(
    package_id: int,
    data: PackageUpdate,
    db: Session
):
    # Tìm Package
    package = db.query(Package).filter(
        Package.id == package_id
    ).first()

    # Không tìm thấy
    if not package:
        raise HTTPException(
            status_code=404,
            detail="Kiện hàng không tồn tại"
        )

    try:
        # Chỉ lấy những trường người dùng
        # thực sự gửi lên
        update_data = data.model_dump(
            exclude_unset=True
        )

        # Cập nhật từng thuộc tính
        for key, value in update_data.items():
            setattr(
                package,
                key,
                value
            )

        # Lưu database
        db.commit()

        # Đồng bộ dữ liệu mới nhất
        db.refresh(package)

        return package

    except Exception:
        # Có lỗi thì rollback
        db.rollback()
        raise


# ==========================================
# 4. XÓA WAYBILL
# ==========================================

def delete_waybill(
    waybill_id: int,
    db: Session
):
    # Tìm Waybill
    waybill = db.query(Waybill).filter(
        Waybill.id == waybill_id
    ).first()

    # Không tìm thấy
    if not waybill:
        raise HTTPException(
            status_code=404,
            detail="Vận đơn không tồn tại"
        )

    try:
        # Hard Delete
        db.delete(waybill)

        # Lưu thay đổi
        db.commit()

        return {
            "message": "Xóa vận đơn thành công",
            "waybill_id": waybill_id
        }

    except Exception:
        # Có lỗi thì rollback
        db.rollback()
        raise