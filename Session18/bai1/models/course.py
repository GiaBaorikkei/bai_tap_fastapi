from sqlalchemy import Column, Integer, String

from bai1.database.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    max_students = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="OPEN"
    )