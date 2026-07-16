from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#  ĐỊA CHỈ CỦA DATABASE

DATABASE_URL = "mysql+pymysql://root:21082005@localhost:3306/connect_db"

# engine: cánh của để mở ra truy cập vào db
engine = create_engine(DATABASE_URL)
 
# Tạo phiên làm việc mỗi lần tương tác database
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit= False,
    bind=engine
)

# Viết hàm để làm việc với db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
