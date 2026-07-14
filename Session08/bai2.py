from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional, Literal
import re

app = FastAPI()

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY"
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY"
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING"
    }
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

# ==========================
# MODEL
# ==========================

class AssetCreate(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: Literal["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(gt=0)
    start_date: str
    duration_months: int = Field(ge=1, le=12)


# ==========================
# ASSET API
# ==========================

@app.post("/assets", status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate):

    for item in assets:
        if item["serial_number"].lower() == asset.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = asset.model_dump()
    new_asset["id"] = len(assets) + 1

    assets.append(new_asset)

    return new_asset


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_stock: Optional[int] = Query(None, ge=0)
):

    result = assets

    if keyword:
        result = [
            a for a in result
            if keyword.lower() in a["serial_number"].lower()
            or keyword.lower() in a["model"].lower()
        ]

    if status:
        result = [
            a for a in result
            if a["status"] == status
        ]

    if min_stock is not None:
        result = [
            a for a in result
            if a["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):

    for asset in assets:
        if asset["id"] == asset_id:
            return asset

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset: AssetCreate):

    for index, item in enumerate(assets):

        if item["id"] == asset_id:

            for a in assets:
                if (
                    a["id"] != asset_id
                    and a["serial_number"].lower() == asset.serial_number.lower()
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Serial number already exists"
                    )

            update_data = asset.model_dump()
            update_data["id"] = asset_id

            assets[index] = update_data

            return update_data

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):

    for index, asset in enumerate(assets):

        if asset["id"] == asset_id:
            assets.pop(index)
            return {
                "message": "Deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


# ==========================
# ALLOCATION API
# ==========================

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


@app.post("/allocations", status_code=status.HTTP_201_CREATED)
def create_allocation(allocation: AllocationCreate):

    asset = None

    for a in assets:
        if a["id"] == allocation.asset_id:
            asset = a
            break

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not ready"
        )

    if allocation.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    if not re.fullmatch(EMAIL_REGEX, allocation.employee_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    new_allocation = allocation.model_dump()
    new_allocation["id"] = len(allocations) + 1

    allocations.append(new_allocation)

    # Trừ số lượng tồn kho
    asset["stock_available"] -= allocation.allocated_quantity

    # Nếu hết hàng thì cập nhật trạng thái
    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return new_allocation


@app.get("/allocations")
def get_allocations():
    return allocations