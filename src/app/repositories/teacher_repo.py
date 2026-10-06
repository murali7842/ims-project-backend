from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.base import BaseRepo


class TeacherRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    async def get_all_teacher(self, search: str | None, page: int, size: int, db: AsyncSession):
        query = (
            select(User)
            .options(selectinload(User.institution))
            .where(User.role == UserRole.TEACHER))

        if search:
            search_term = f"%{search.strip()}%"

            query = query.where(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone_number.ilike(search_term)
                )
            )

        # Total count query
        count_query = (
            select(func.count())
            .select_from(query.subquery())
        )

        total_elements = await db.scalar(count_query)

        # Pagination
        query = (
            query
            .offset((page - 1) * size)
            .limit(size)
            .order_by(User.id.desc())
        )

        result = await db.execute(query)

        teachers = result.scalars().all()

        return teachers, total_elements

    async def get_by_id(self, teacher_id: int, db: AsyncSession) -> User | None:
        """Get teacher by ID with institution loaded"""
        query = (
            select(User)
            .options(selectinload(User.institution))
            .where(
                User.id == teacher_id,
                User.role == UserRole.TEACHER
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
