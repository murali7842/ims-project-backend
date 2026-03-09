from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.course import Course
from src.app.repositories.base import BaseRepo


class CourseRepo(BaseRepo[Course]):

    def __init__(self):
        super().__init__(Course)

    async def exist_by_name(self, name: str, session: AsyncSession) -> bool:
        query = select(func.count(Course.id)).where(Course.name == name)
        result = await session.execute(query)
        return result.scalar() > 0
