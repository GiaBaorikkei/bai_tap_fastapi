"""
1. ĐỊA CHỈ CỦA DATABASE
2. ENGINE TỪ CREATE_ENGINE
3. SESSIONLOCAL TỪ SESSION_MAKER
4. HÀM GET_DB
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/manager_student"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush= False,
    autocommit =False,
    bind= engine
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

