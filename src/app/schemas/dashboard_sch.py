from datetime import datetime

from pydantic import BaseModel

from src.app.models.enum import UserRole
from src.app.models.institution import Institution


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
