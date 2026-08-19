from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app.database import (
    engine,
    Base,
    get_db
)

from app.schemas import (
    WarehouseCreate,
    WarehouseDetailResponse,
    PackageUpdate,
    PackageResponse,
    WaybillResponse
)

from app.service import (
    create_warehouse,
    get_warehouse_detail,
    update_package,
    delete_waybill
)


# ==========================================
# CREATE TABLE
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# FASTAPI
# ==========================================

app = FastAPI()


# ==========================================
# 1. CREATE WAREHOUSE
# ==========================================

@app.post(
    "/warehouses",
    response_model=WarehouseDetailResponse,
    status_code=status.HTTP_201_CREATED
)
def create_warehouse_api(
    data: WarehouseCreate,
    db: Session = Depends(get_db)
):

    return create_warehouse(
        data,
        db
    )


# ==========================================
# 2. GET WAREHOUSE DETAIL
# ==========================================

@app.get(
    "/warehouses/{warehouse_id}",
    response_model=WarehouseDetailResponse,
    status_code=status.HTTP_200_OK
)
def get_warehouse_api(
    warehouse_id: int,
    db: Session = Depends(get_db)
):

    return get_warehouse_detail(
        warehouse_id,
        db
    )


# ==========================================
# 3. PATCH PACKAGE
# ==========================================

@app.patch(
    "/packages/{package_id}",
    response_model=PackageResponse,
    status_code=status.HTTP_200_OK
)
def update_package_api(
    package_id: int,
    data: PackageUpdate,
    db: Session = Depends(get_db)
):

    return update_package(
        package_id,
        data,
        db
    )


# ==========================================
# 4. DELETE WAYBILL
# ==========================================

@app.delete(
    "/waybills/{waybill_id}",
    status_code=status.HTTP_200_OK
)
def delete_waybill_api(
    waybill_id: int,
    db: Session = Depends(get_db)
):

    return delete_waybill(
        waybill_id,
        db
    )