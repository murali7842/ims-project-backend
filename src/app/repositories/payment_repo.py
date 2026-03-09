from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.payment import Payment
from src.app.repositories.base import BaseRepo


class PaymentRepo(BaseRepo[Payment]):

    def __init__(self):
        super().__init__(Payment)

