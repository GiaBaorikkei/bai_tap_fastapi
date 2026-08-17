from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Fleet(Base):
    __tablename__ = 'fleet'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Quan hệ 1-N: Một Fleet có nhiều Driver
    drivers = relationship("Driver", back_populates="fleet")


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), nullable=False)
    status = Column(String(20)) 

    # Quan hệ N-N: Đồng bộ hai chiều với Driver thông qua bảng trung gian 'booking'
    drivers = relationship("Driver", secondary="booking", back_populates="cars")


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    # Khóa ngoại liên kết tới Driver và Car
    driver_id = Column(Integer, ForeignKey('driver.id'))
    car_id = Column(Integer, ForeignKey('car.id'))


class Driver(Base):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20)) # ACTIVE hoặc INACTIVE
    
    # Khóa ngoại liên kết tới Fleet (phía 'Nhiều' chứa khóa ngoại)
    fleet_id = Column(Integer, ForeignKey('fleet.id'))

    # Quan hệ 1-N: Liên kết trả về object Fleet
    fleet = relationship("Fleet", back_populates="drivers")

    # Quan hệ N-N: Lấy danh sách các Car thông qua bảng trung gian 'booking'
    cars = relationship("Car", secondary="booking", back_populates="drivers")