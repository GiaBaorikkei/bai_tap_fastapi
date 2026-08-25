from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class MenuStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class MenuItemCreate(BaseModel):
    dish_code: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    dish_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    calorie_count: int = Field(
        ...,
        gt=0
    )

    price: float = Field(
        ...,
        gt=0
    )

    status: MenuStatus = MenuStatus.AVAILABLE


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    dish_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    calorie_count: Optional[int] = Field(
        default=None,
        gt=0
    )

    price: Optional[float] = Field(
        default=None,
        gt=0
    )

    status: Optional[MenuStatus] = None


class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: MenuStatus

    model_config = ConfigDict(
        from_attributes=True
    )


class ApiResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[object] = None
    path: str
    timestamp: str