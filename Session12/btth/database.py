from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Địa chỉ của database
DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/session12_db"

#engine: cánh cửa mở ra truy cập vào db
engine = create_engine(DATABASE_URL)

# Tạo phiên làm việc mỗi lần tương tác database
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit= False,
    bind=engine
)

# Hàm làm việc với db
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()