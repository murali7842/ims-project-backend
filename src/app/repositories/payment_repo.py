from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.models.payment import Payment
from src.app.models.student import Student
from src.app.repositories.base import BaseRepo
from src.app.schemas.payment_sch import PaymentSortBy


class PaymentRepo(BaseRepo[Payment]):

    def __init__(self):
        super().__init__(Payment)

    async def get_all_payments(self, search: str | None, institution_id: int | None, student_id: int | None,
                               sort_by: PaymentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> tuple[list[Payment], int]:
        query = select(Payment)

        # payment has no institution column, so institution and search both go through the student (joined once)
        if institution_id is not None or search:
            query = query.join(Student, Payment.student_id == Student.id)

        if institution_id is not None:
            query = query.where(Student.institution_id == institution_id)

        if student_id is not None:
            query = query.where(Payment.student_id == student_id)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Student.name.ilike(search_term),
                    Payment.payment_mode.ilike(search_term),
                    Payment.remarks.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(Payment, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # Payment.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, Payment.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements
