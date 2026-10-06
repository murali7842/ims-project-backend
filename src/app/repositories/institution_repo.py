from sqlalchemy import select, func, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.models.institution import Institution
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