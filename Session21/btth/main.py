from fastapi import FastAPI

from database import Base, engine
from auth_router import router


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="JWT Authentication API"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "JWT Authentication API"
    }