from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.operator_sch import CreateOperatorSch


class OperatorService(ABC):

    @abstractmethod
    async def create_operator(self, sch: CreateOperatorSch, db: AsyncSession) -> int:
        pass