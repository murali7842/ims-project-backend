from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.teacher_sch import CreateTeacherSch


class TeacherService(ABC):

    @abstractmethod
    async def create_teacher(self, sch: CreateTeacherSch, db: AsyncSession) -> int:
        pass