from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.course_sch import CreateCourseSch,GetCourseSch


class CourseService(ABC):

    @abstractmethod
    async def create_course(self, sch: CreateCourseSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_course_by_id(self, course_id : int, db : AsyncSession) -> GetCourseSch:
        pass
