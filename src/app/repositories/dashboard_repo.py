from datetime import datetime

from sqlalchemy import select, func, literal, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import UserRole
from src.app.models.institution import Institution
from src.app.models.student import Student
from src.app.models.user import User


class DashboardRepo:

    async def get_summary_counts(self, institution_id: int | None, db: AsyncSession):
        institution_query = select(func.count(Institution.id))
        operator_query = select(func.count(User.id)).where(User.role == UserRole.OPERATOR)
        teacher_query = select(func.count(User.id)).where(User.role == UserRole.TEACHER)
        student_query = select(func.count(Student.id))

        if institution_id is not None:
            institution_query = institution_query.where(Institution.id == institution_id)
            operator_query = operator_query.where(User.institution_id == institution_id)
            teacher_query = teacher_query.where(User.institution_id == institution_id)
            student_query = student_query.where(Student.institution_id == institution_id)

        # all four counts as scalar subqueries -> a single DB round trip
        query = select(
            institution_query.scalar_subquery().label("total_institutions"),
            operator_query.scalar_subquery().label("total_operators"),
            teacher_query.scalar_subquery().label("total_teachers"),
            student_query.scalar_subquery().label("total_students"),
        )
        result = await db.execute(query)
        return result.mappings().one()

    async def get_users_count_by_role(self, institution_id: int | None, start: datetime | None,
                                      end: datetime | None, db: AsyncSession) -> list[tuple[str, int]]:
        user_query = select(User.role.label("role"), func.count(User.id).label("count"))
        # students live in their own table, so they are counted separately and merged with UNION ALL
        student_query = select(literal(UserRole.STUDENT.value).label("role"), func.count(Student.id).label("count"))

        if institution_id is not None:
            user_query = user_query.where(User.institution_id == institution_id)
            student_query = student_query.where(Student.institution_id == institution_id)

        # range filter (instead of extract month/year) so an index on created_at can be used
        if start is not None:
            user_query = user_query.where(User.created_at >= start, User.created_at < end)
            student_query = student_query.where(Student.created_at >= start, Student.created_at < end)

        query = union_all(user_query.group_by(User.role), student_query)
        result = await db.execute(query)
        return [(row.role, row.count) for row in result]

    async def get_recent_institutions(self, institution_id: int | None, limit: int,
                                      db: AsyncSession) -> list[Institution]:
        # id is auto-increment, so ordering by the primary key gives newest first using the PK index
        query = select(Institution)
        if institution_id is not None:
            query = query.where(Institution.id == institution_id)

        result = await db.execute(query.order_by(Institution.id.desc()).limit(limit))
        return list(result.scalars().all())

    async def get_recent_users(self, institution_id: int | None, limit: int, db: AsyncSession):
        # select only the columns the widget needs
        query = select(User.id, User.name, User.email, User.role, User.created_at)
        if institution_id is not None:
            query = query.where(User.institution_id == institution_id)

        result = await db.execute(query.order_by(User.id.desc()).limit(limit))
        return result.all()

    async def get_institution_dropdown(self, institution_id: int | None, db: AsyncSession):
        query = select(Institution.id, Institution.name)
        if institution_id is not None:
            query = query.where(Institution.id == institution_id)

        result = await db.execute(query.order_by(Institution.name.asc()))
        return result.all()
