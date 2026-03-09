from datetime import datetime

from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from src.app.config.db_config import Base
from src.app.models.base import Auditable
from src.app.models.enum import UserRole


class User(Base, Auditable):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    address: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, native_enum=False, length=20)
    )
    institution_id: Mapped[int | None] = mapped_column(ForeignKey("institution.id", ondelete="CASCADE"))  # FK to Institution

    institution: Mapped["Institution"] = relationship("Institution", back_populates="operators")

    courses_teacher: Mapped["Course"] = relationship("Course", back_populates="teacher")



class OTPRecord(Base, Auditable):
    __tablename__ = "otp_records"

    email: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    otp: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)