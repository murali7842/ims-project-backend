from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.config.db_config import Base
from src.app.models.base import Auditable


class Course(Base, Auditable):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    duration: Mapped[str] = mapped_column(String(100), nullable=True)
    course_fee: Mapped[float] = mapped_column(default=0.0)
    institution_id: Mapped[int | None] = mapped_column(ForeignKey("institution.id", ondelete="CASCADE"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))


    institution_course: Mapped["Institution"] = relationship("Institution", back_populates="courses")
    teacher: Mapped["User"] = relationship("User", back_populates="courses_teacher")
    batches: Mapped[list["Batch"]] = relationship("Batch", back_populates="course", cascade="all, delete")
