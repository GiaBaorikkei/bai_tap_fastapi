from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import Base, engine
from routers import router


Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ",
            "error": "Validation Error",
            "data": exc.errors(),
            "path": request.url.path,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat().replace("+00:00", "Z")
        }
    )



@app.get("/")
def root():
    return {
        "message": "Catering Menu Management API is running"
    }

app.include_router(router)