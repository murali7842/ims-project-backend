from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models.enum import UserRole, SortOrder
from src.app.models.user import User
from src.app.repositories.base import BaseRepo
from src.app.schemas.operator_sch import OperatorSortBy


class OperatorRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    async def get_all_operators(self, search: str | None, sort_by: OperatorSortBy, sort_order: SortOrder,
                                page: int, size: int, db: AsyncSession) -> tuple[list[User], int]:
        query = select(User).where(User.role == UserRole.OPERATOR)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone_number.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(User, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # User.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .options(selectinload(User.institution))
            .order_by(order, User.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements
