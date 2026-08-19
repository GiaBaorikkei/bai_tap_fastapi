from sqlalchemy import Column, Integer, String, ForeignKey

from btth.database.base import Base


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

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )