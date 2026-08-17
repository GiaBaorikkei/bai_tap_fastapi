from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Any


class MenuItemCreate(BaseModel):
    dish_code: str
    dish_name: str = Field(min_length=1)
    calorie_count: int = Field(gt=0)
    price: float = Field(gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"]


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = None
    dish_name: Optional[str] = Field(default=None, min_length=1)
    calorie_count: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)
    status: Optional[Literal["AVAILABLE", "OUT_OF_STOCK"]] = None


class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str]
    data: Optional[Any]
    path: str
    timestamp: str