from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User
from src.app.repositories.base import BaseRepo


class OperatorRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)
