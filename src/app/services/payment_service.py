from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.payment_sch import CreatePaymentSch


class PaymentService(ABC):

    @abstractmethod
    async def create_payment(self, sch: CreatePaymentSch, db: AsyncSession) -> int:
        pass