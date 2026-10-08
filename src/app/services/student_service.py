from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.schemas.student_sch import CreateStudentSch, GetStudentSch, UpdateStudentSch, StudentSortBy
from src.app.models.user import User
from src.app.shared.response import PaginationResponse


class StudentService(ABC):

    @abstractmethod
    async def create_student(self, sch: CreateStudentSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_student_by_id(self, student_id: int, db: AsyncSession) -> GetStudentSch:
        pass

    @abstractmethod
    async def get_all_students(self, user: User, search: str | None, institution_id: int | None,
                               course_id: int | None, batch_id: int | None,
                               sort_by: StudentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> PaginationResponse[GetStudentSch]:
        pass

    @abstractmethod
    async def update_student(self, sch: UpdateStudentSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_student(self, student_id: int, db: AsyncSession) -> str:
        pass
