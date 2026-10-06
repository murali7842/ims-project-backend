from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import SortOrder
from src.app.schemas.operator_sch import CreateOperatorSch, GetOperatorSch, UpdateOperatorSch, OperatorSortBy
from src.app.shared.response import PaginationResponse


class OperatorService(ABC):

    @abstractmethod
    async def create_operator(self, sch: CreateOperatorSch, db: AsyncSession) -> int:
        pass

    @abstractmethod
    async def get_operator_by_id(self, operator_id: int, db: AsyncSession) -> GetOperatorSch:
        pass

    @abstractmethod
    async def get_all_operators(self, search: str | None, sort_by: OperatorSortBy, sort_order: SortOrder,
                                page: int, size: int, db: AsyncSession) -> PaginationResponse[GetOperatorSch]:
        pass

    @abstractmethod
    async def update_operator(self, sch: UpdateOperatorSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_operator(self, operator_id: int, db: AsyncSession) -> str:
        pass
