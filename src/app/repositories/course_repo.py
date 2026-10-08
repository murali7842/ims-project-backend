from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.course import Course
from src.app.models.enum import SortOrder
from src.app.repositories.base import BaseRepo
from src.app.schemas.course_sch import CourseSortBy


class CourseRepo(BaseRepo[Course]):

    def __init__(self):
        super().__init__(Course)

    async def exist_by_name(self, name: str, session: AsyncSession, exclude_id: int | None = None) -> bool:
        query = select(Course.id).where(Course.name == name)
        if exclude_id is not None:
            query = query.where(Course.id != exclude_id)
        return await session.scalar(query.limit(1)) is not None

    async def get_all_courses(self, search: str | None, institution_id: int | None,
                              sort_by: CourseSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> tuple[list[Course], int]:
        query = select(Course)

        if institution_id is not None:
            query = query.where(Course.institution_id == institution_id)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Course.name.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(Course, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # Course.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, Course.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements

    async def update_by_id(self, course_id: int, data: dict, db: AsyncSession) -> bool:
        result = await db.execute(update(Course).where(Course.id == course_id).values(**data))
        await db.commit()
        return result.rowcount > 0
