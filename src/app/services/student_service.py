from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.student_sch import CreateStudentSch


class StudentService(ABC):

    @abstractmethod
    async def create_student(self, sch: CreateStudentSch, db: AsyncSession) -> int:
        pass