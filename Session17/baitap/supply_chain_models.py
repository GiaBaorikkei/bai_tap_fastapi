from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

# Khởi tạo lớp Base
Base = declarative_base()

# BẢNG TRUNG GIAN (ASSOCIATION TABLE) CHO QUAN HỆ NHIỀU - NHIỀU (N-N)
# Lưu ý: Bảng này được định nghĩa bằng đối tượng Table, không phải Class Model
package_truck = Table(
    'package_truck',
    Base.metadata,
    Column('package_id', Integer, ForeignKey('packages.id'), primary_key=True),
    Column('truck_id', Integer, ForeignKey('trucks.id'), primary_key=True)
)

# THỰC THỂ 1: WAREHOUSE (NHÀ KHO)
class Warehouse(Base):
    __tablename__ = 'warehouses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    
    # Quan hệ 1-N: Một Nhà kho chứa nhiều Kiện hàng
    packages = relationship("Package", back_populates="warehouse")

# THỰC THỂ 2: PACKAGE (KIỆN HÀNG)
class Package(Base):
    __tablename__ = 'packages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_code = Column(String(50), unique=True, nullable=False)
    weight = Column(Float, nullable=False)
    
    # KHÓA NGOẠI: Phía "Nhiều" của quan hệ 1-N với Warehouse
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    
    # Quan hệ N-1: Trỏ ngược lại Warehouse
    warehouse = relationship("Warehouse", back_populates="packages")
    
    # Quan hệ 1-1: Một Kiện hàng có duy nhất Một Vận đơn
    # Ràng buộc uselist=False đảm bảo trả về đối tượng đơn lẻ thay vì List
    waybill = relationship("Waybill", back_populates="package", uselist=False)
    
    # Quan hệ N-N: Kiện hàng được vận chuyển qua nhiều Xe tải
    # Tham số secondary trỏ đến bảng trung gian package_truck
    trucks = relationship("Truck", secondary=package_truck, back_populates="packages")


# THỰC THỂ 3: WAYBILL (VẬN ĐƠN CHI TIẾT)
class Waybill(Base):
    __tablename__ = 'waybills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(100), nullable=False)
    shipping_status = Column(String(50), nullable=False)
    
    # KHÓA NGOẠI: Phía bảng phụ của quan hệ 1-1 với Package
    # BẮT BUỘC unique=True để đảm bảo tính độc bản (Mỗi vận đơn chỉ thuộc về 1 kiện hàng)
    package_id = Column(Integer, ForeignKey('packages.id'), unique=True, nullable=False)
    
    # Quan hệ 1-1: Trỏ ngược lại Package
    package = relationship("Package", back_populates="waybill")


# THỰC THỂ 4: TRUCK (XE TẢI VẬN CHUYỂN)
class Truck(Base):
    __tablename__ = 'trucks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    license_plate = Column(String(20), unique=True, nullable=False)
    
    # Quan hệ N-N: Xe tải bốc dỡ nhiều Kiện hàng
    # Tham số secondary trỏ đến bảng trung gian package_truck
    packages = relationship("Package", secondary=package_truck, back_populates="trucks")