from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cấu hình database

DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/course_management"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit= False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()