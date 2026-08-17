from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Nơi cấu hình database
""" 
1. URL
2. engine
3. SesionLocal
4. get_db

"""
DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/fastapi"

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