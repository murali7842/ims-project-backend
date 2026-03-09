from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_auth_service
from src.app.schemas.auth_sch import TokenSch, RefreshToken, PasswordRecoveryRequest, ResetPasswordRequest
from src.app.services.auth_service import AuthService
from src.app.shared.response import Response

authRouter = APIRouter()


@authRouter.post("/login", response_model=TokenSch, name="User Login Service")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
        db: AsyncSession = Depends(get_db)
):
    tokens = await auth_service.authenticate_user(form_data.username, form_data.password,db)
    return tokens

@authRouter.post("/refresh-token", response_model=Response[TokenSch], name="Refresh Token")
async def refresh_token(
        token: RefreshToken,
        auth_service: AuthService = Depends(get_auth_service),
        db: AsyncSession = Depends(get_db)
):
    tokens = await auth_service.refresh_tokens(token.refresh_token, db)
    return Response[TokenSch](body=tokens)

@authRouter.post("/forgot-password", response_model=Response[str], name="Forgot Password")
async def forgot_password(
        request: PasswordRecoveryRequest,
        background_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(get_auth_service),
        db: AsyncSession = Depends(get_db),
):
    forgot = await auth_service.forgot_password(request, db, background_tasks)
    return Response[str](body=forgot)

@authRouter.post("/reset-password", response_model=Response[str], name="Reset Password")
async def reset_password(
        request: ResetPasswordRequest,
        auth_service: AuthService = Depends(get_auth_service),
        db: AsyncSession = Depends(get_db),
):
    reset = await auth_service.reset_password(request, db)
    return Response[str](body=reset, msg="Password reset successfully", msg_code="success.password.reset")