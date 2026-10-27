from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.batch import Batch
from src.app.models.course import Course
from src.app.models.institution import Institution
from src.app.models.student import Student
from src.app.models.enum import SortOrder
from src.app.repositories.base import BaseRepo
from src.app.schemas.batch_sch import BatchSortBy


class BatchRepo(BaseRepo[Batch]):

    def __init__(self):
        super().__init__(Batch)

    async def exist_by_name(self, name: str, session: AsyncSession, exclude_id: int | None = None) -> bool:
        query = select(Batch.id).where(Batch.name == name)
        if exclude_id is not None:
            query = query.where(Batch.id != exclude_id)
        return await session.scalar(query.limit(1)) is not None

    async def get_all_batches(self, search: str | None, institution_id: int | None, teacher_id: int | None,
                              sort_by: BatchSortBy, sort_order: SortOrder,
                              page: int, size: int, db: AsyncSession) -> tuple[list[Batch], int]:
        query = select(Batch)

        if institution_id is not None:
            query = query.where(Batch.institution_id == institution_id)
        if teacher_id is not None:
            query = query.where(Batch.course_id.in_(select(Course.id).where(Course.teacher_id == teacher_id)))

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Batch.name.ilike(search_term),
                    Batch.timing.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(Batch, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # Batch.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, Batch.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements

    async def update_by_id(self, batch_id: int, data: dict, db: AsyncSession) -> bool:
        result = await db.execute(update(Batch).where(Batch.id == batch_id).values(**data))
        await db.commit()
        return result.rowcount > 0

    async def delete_by_id(self, batch_id: int, db: AsyncSession) -> bool:
        result = await db.execute(delete(Batch).where(Batch.id == batch_id))
        await db.commit()
        return result.rowcount > 0

    async def get_batch_details(self, batch_id: int, db: AsyncSession):
        """Batch with course name, institution name and enrolled student count in a single query"""
        total_students = (
            select(func.count(Student.id))
            .where(Student.batch_id == Batch.id)
            .correlate(Batch)
            .scalar_subquery()
        )
        query = (
            select(Batch, Course.name.label("course_name"), Institution.name.label("institution_name"),
                   total_students.label("total_students"), Course.teacher_id.label("teacher_id"))
            .outerjoin(Course, Batch.course_id == Course.id)
            .outerjoin(Institution, Batch.institution_id == Institution.id)
            .where(Batch.id == batch_id)
        )
        result = await db.execute(query)
        return result.first()
