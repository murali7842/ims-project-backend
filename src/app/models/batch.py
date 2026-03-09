from datetime import date
from sqlalchemy import String, ForeignKey, Integer, Date, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.config.db_config import Base
from src.app.models.base import Auditable
from src.app.models.enum import BatchMode


class Batch(Base, Auditable):
    __tablename__ = "batch"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    timing: Mapped[str] = mapped_column(String(100), nullable=False)
    student_limit: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    mode: Mapped[BatchMode] = mapped_column(Enum(BatchMode), nullable=False)

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"))
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id", ondelete="CASCADE"))

    course: Mapped["Course"] = relationship("Course", back_populates="batches")
    institutions: Mapped["Institution"] = relationship("Institution", back_populates="batches")
    # students: Mapped[list["User"]] = relationship("User", secondary="batch_students", back_populates="batches")
    # teachers: Mapped[list["User"]] = relationship("User", secondary="batch_teachers", back_populates="teaching_batches")
