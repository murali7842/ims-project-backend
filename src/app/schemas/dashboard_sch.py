from datetime import datetime, date

from pydantic import BaseModel

from src.app.models.enum import UserRole, BatchMode, PublishStatus
from src.app.models.institution import Institution
from src.app.schemas.base import DropDownSch


class DashboardSummarySch(BaseModel):
    total_institutions: int
    total_operators: int
    total_teachers: int
    total_students: int


class RoleCountSch(BaseModel):
    role: UserRole
    count: int


class RecentInstitutionSch(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime | None

    @staticmethod
    def from_entity(entity: Institution) -> "RecentInstitutionSch":
        return RecentInstitutionSch(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            created_at=entity.created_at
        )


class RecentUserSch(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    created_at: datetime | None


class TeacherBatchSch(BaseModel):
    id: int
    name: str
    course: DropDownSch | None
    timing: str
    mode: BatchMode
    start_date: date
    end_date: date
    student_limit: int
    total_students: int


class TeacherExamSch(BaseModel):
    id: int
    title: str
    status: PublishStatus
    start_date: date | None
    end_date: date | None
    course: DropDownSch | None


class TeacherDashboardSch(BaseModel):
    total_courses: int
    total_batches: int
    total_students: int
    upcoming_exams: int
    batches: list[TeacherBatchSch]
    recent_exams: list[TeacherExamSch]
