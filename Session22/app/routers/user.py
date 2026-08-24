from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.user import get_user, create_user
from app.schemas.user import CreateUser

router_user = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router_user.get("")
def get_all_user(db: Session = Depends(get_db)):
    return get_user(db)

@router_user.post("")
def add_user(user:CreateUser, db: Session = Depends(get_db)):
    return create_user(user, db)