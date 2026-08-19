"""
VIẾT API VỀ MỐI QUAN HỆ 1-N
"""

from fastapi import FastAPI
from src.routers.category import router_category
from src.routers.product import router_product

app = FastAPI()
app.include_router(router_category)
app.include_router(router_product)

@app.get("/")
def home():
    return {
        "message": "API đang chạy!"
    }   