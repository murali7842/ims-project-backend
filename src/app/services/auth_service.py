from abc import ABC, abstractmethod
from fastapi import BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.auth_sch import TokenSch, PasswordRecoveryRequest, ResetPasswordRequest


class AuthService(ABC):

    @abstractmethod
    async def authenticate_user(self, email: str, password: str, db: AsyncSession)-> TokenSch:
        pass

    @abstractmethod
    async def refresh_tokens(self, refresh_token: str, db: AsyncSession) -> TokenSch:
        pass

    @abstractmethod
    async def forgot_password(self, request: PasswordRecoveryRequest, db: AsyncSession,
                              background_tasks: BackgroundTasks) -> str:
        pass

    @abstractmethod
    async def reset_password(self, request: ResetPasswordRequest, db: AsyncSession) -> str:
        pass

