from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.models.student import Student
from src.app.repositories.base import BaseRepo
from src.app.schemas.student_sch import StudentSortBy


class StudentRepo(BaseRepo[Student]):

    def __init__(self):
        super().__init__(Student)

    async def get_conflicting_student(self, email: str, phone_number: str, db: AsyncSession,
                                      exclude_id: int | None = None) -> Student | None:
        """Any other student already holding this email or phone number (both are unique columns)"""
        query = select(Student).where(or_(Student.email == email, Student.phone_number == phone_number))
        if exclude_id is not None:
            query = query.where(Student.id != exclude_id)
        return await db.scalar(query.limit(1))

    async def get_all_students(self, search: str | None, course_id: int | None, batch_id: int | None,
                               sort_by: StudentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> tuple[list[Student], int]:
        query = select(Student)

        if course_id is not None:
            query = query.where(Student.course_id == course_id)
        if batch_id is not None:
            query = query.where(Student.batch_id == batch_id)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Student.name.ilike(search_term),
                    Student.email.ilike(search_term),
                    Student.phone_number.ilike(search_term),
                    Student.guardian_name.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(Student, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # Student.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, Student.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements
