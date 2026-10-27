from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.batch import Batch
from src.app.models.course import Course
from src.app.models.enum import SortOrder, UserRole
from src.app.models.institution import Institution
from src.app.models.student import Student
from src.app.models.user import User
from src.app.repositories.base import BaseRepo
from src.app.schemas.institution_sch import InstitutionSortBy


class InstitutionRepo(BaseRepo[Institution]):

    def __init__(self):
        super().__init__(Institution)

    async def is_institution_exists(self, name: str, db: AsyncSession, exclude_id: int | None = None) -> bool:
        query = select(Institution.id).where(Institution.name.ilike(name))
        if exclude_id is not None:
            query = query.where(Institution.id != exclude_id)
        return await db.scalar(query.limit(1)) is not None

    async def exist_by_email(self, email: str, db: AsyncSession, exclude_id: int | None = None) -> bool:
        query = select(Institution.id).where(Institution.email == email)
        if exclude_id is not None:
            query = query.where(Institution.id != exclude_id)
        return await db.scalar(query.limit(1)) is not None

    async def get_multiple(self, ids: list[int], db: AsyncSession):
        stmt = select(Institution).where(Institution.id.in_(ids))
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all_institutions(self, search: str | None, sort_by: InstitutionSortBy, sort_order: SortOrder,
                                   page: int, size: int, db: AsyncSession) -> tuple[list[Institution], int]:
        query = select(Institution)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Institution.name.ilike(search_term),
                    Institution.email.ilike(search_term),
                    Institution.contact_number.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(Institution, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # Institution.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, Institution.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements

    async def get_institution_details(self, institution_id: int, db: AsyncSession):
        """Institution with all its totals as scalar subqueries -> a single DB round trip"""
        def count(column, *conditions):
            return select(func.count(column)).where(*conditions).scalar_subquery()

        query = select(
            Institution,
            count(Course.id, Course.institution_id == institution_id).label("total_courses"),
            count(Batch.id, Batch.institution_id == institution_id).label("total_batches"),
            count(User.id, User.institution_id == institution_id,
                  User.role == UserRole.TEACHER).label("total_teachers"),
            count(User.id, User.institution_id == institution_id,
                  User.role == UserRole.OPERATOR).label("total_operators"),
            count(Student.id, Student.institution_id == institution_id).label("total_students"),
        ).where(Institution.id == institution_id)
        result = await db.execute(query)
        return result.first()

    async def get_institution_courses_with_batches(self, institution_id: int, db: AsyncSession):
        """Flat (course, teacher, batch) rows for all courses of an institution; courses without batches
        come with batch NULL"""
        query = (
            select(Course.id.label("course_id"), Course.name.label("course_name"), Course.course_fee,
                   User.id.label("teacher_id"), User.name.label("teacher_name"),
                   Batch.id.label("batch_id"), Batch.name.label("batch_name"))
            .outerjoin(User, Course.teacher_id == User.id)
            .outerjoin(Batch, Batch.course_id == Course.id)
            .where(Course.institution_id == institution_id)
            .order_by(Course.id, Batch.id)
        )
        result = await db.execute(query)
        return result.all()
