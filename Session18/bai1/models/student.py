from sqlalchemy import Column, Integer, String

from bai1.database.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True
    )

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )