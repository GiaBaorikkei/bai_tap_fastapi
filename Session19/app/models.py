from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    warehouse_name = Column(
        String(100),
        nullable=False
    )

    location = Column(
        String(255),
        nullable=False
    )

    # Quan hệ 1-N
    # Một Warehouse có nhiều Package
    packages = relationship(
        "Package",
        back_populates="warehouse"
    )


class Package(Base):
    __tablename__ = "packages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    package_code = Column(
        String(100),
        nullable=False,
        unique=True
    )

    weight = Column(
        Float,
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    # Package thuộc về một Warehouse
    warehouse = relationship(
        "Warehouse",
        back_populates="packages"
    )

    # Quan hệ 1-1
    waybill = relationship(
        "Waybill",
        back_populates="package",
        uselist=False
    )


class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tracking_number = Column(
        String(100),
        nullable=False,
        unique=True
    )

    shipping_status = Column(
        String(50),
        nullable=False
    )

    package_id = Column(
        Integer,
        ForeignKey("packages.id"),
        nullable=False,
        unique=True
    )

    # Waybill thuộc về một Package
    package = relationship(
        "Package",
        back_populates="waybill"
    )