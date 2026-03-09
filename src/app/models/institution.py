from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.config.db_config import Base
from src.app.models.base import Auditable


class Institution(Base,Auditable):
    __tablename__ = "institution"

    id: Mapped[int] = mapped_column(primary_key= True, index=True,  nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str] = mapped_column(String(255))
    contact_number: Mapped[str | None] = mapped_column(String(15))

    operators: Mapped[list["User"]] = relationship("User", back_populates="institution")
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="institution_course")
    batches: Mapped[list["Batch"]] = relationship("Batch", back_populates="institutions", cascade="all, delete")
    assessment_publishes: Mapped[list["AssessmentInstitutionPublish"]] = relationship(
            "AssessmentInstitutionPublish", back_populates="institution"
        )

