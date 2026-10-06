from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.schemas.course_sch import CreateCourseSch, GetCourseSch, UpdateCourseSch, CourseSortBy
from src.app.shared.response import PaginationResponse


class CourseService(ABC):

    @abstractmethod
    async def create_course(self, sch: CreateCourseSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_course_by_id(self, course_id : int, db : AsyncSession) -> GetCourseSch:
        pass

    @abstractmethod
    async def get_all_courses(self, search: str | None, sort_by: CourseSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> PaginationResponse[GetCourseSch]:
        pass

    @abstractmethod
    async def update_course(self, course_id: int, sch: UpdateCourseSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_course(self, course_id: int, db: AsyncSession) -> str:
        pass
