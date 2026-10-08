from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User
from src.app.schemas.teacher_sch import CreateTeacherSch, GetTeacherDetailsSch, UpdateTeacherSch
from src.app.shared.response import PaginationResponse


class TeacherService(ABC):

    @abstractmethod
    async def create_teacher(self, sch: CreateTeacherSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_all_teacher(self, user: User, search: str | None, institution_id: int | None,
                              page: int, size: int, db: AsyncSession) -> PaginationResponse[GetTeacherDetailsSch]:
        pass

    @abstractmethod
    async def get_teacher_by_id(self, teacher_id: int, db: AsyncSession) -> GetTeacherDetailsSch:
        pass

    @abstractmethod
    async def update_teacher(self, sch: UpdateTeacherSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_teacher(self, teacher_id: int, db: AsyncSession) -> str:
        pass
