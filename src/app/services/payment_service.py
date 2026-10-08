from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.schemas.payment_sch import CreatePaymentSch, GetPaymentSch, UpdatePaymentSch, PaymentSortBy
from src.app.models.user import User
from src.app.shared.response import PaginationResponse


class PaymentService(ABC):

    @abstractmethod
    async def create_payment(self, sch: CreatePaymentSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_payment_by_id(self, payment_id: int, db: AsyncSession) -> GetPaymentSch:
        pass

    @abstractmethod
    async def get_all_payments(self, user: User, search: str | None, institution_id: int | None,
                               student_id: int | None,
                               sort_by: PaymentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> PaginationResponse[GetPaymentSch]:
        pass

    @abstractmethod
    async def update_payment(self, sch: UpdatePaymentSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_payment(self, payment_id: int, db: AsyncSession) -> str:
        pass
