from pydantic import BaseModel, ConfigDict
from typing import Optional


# ==========================================
# PACKAGE RESPONSE
# ==========================================

class PackageResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    package_code: str
    weight: float
    warehouse_id: int


# ==========================================
# WAREHOUSE CREATE
# ==========================================

class WarehouseCreate(BaseModel):

    warehouse_name: str
    location: str


# ==========================================
# WAREHOUSE DETAIL RESPONSE
# ==========================================

class WarehouseDetailResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    warehouse_name: str
    location: str

    packages: list[PackageResponse]


# ==========================================
# PACKAGE UPDATE
# ==========================================

class PackageUpdate(BaseModel):

    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None


# ==========================================
# WAYBILL RESPONSE
# ==========================================

class WaybillResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    tracking_number: str
    shipping_status: str
    package_id: int