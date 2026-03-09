import random
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.constant.msg_code import APIMsgCode
from src.app.common.exception import errors
from src.app.config.security import verify_password, create_access_token, create_refresh_token, verify_token, \
    pwd_context, get_password_hash
from src.app.config.setting import get_setting
from src.app.dependencies.db import get_db
from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.repositories.otp_record_repo import OTPRecordRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.auth_sch import TokenSch, PasswordRecoveryRequest, ResetPasswordRequest
from src.app.services.auth_service import AuthService

settings = get_setting()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db),
                           user_repository: UserRepo = Depends()) -> User:
    try:
        # log.debug(f"Received token: {token}")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        # log.debug(f'UserId :: {user_id}')
        if user_id is None:
            raise errors.AuthorizationError(msg="User not found")
    except JWTError:
        raise errors.AuthorizationError(msg="Invalid JWT Token")

    user: User = await user_repository.get(int(user_id), session)
    if user is None:
        raise errors.AuthorizationError(msg="User not found")
    return user

async def create_tokens(user_id: int, email: str) -> TokenSch:
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id, email)
    return TokenSch(access_token=access_token, refresh_token=refresh_token)

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


async def get_admin(user: User = Depends(get_current_active_user)):
    if user.role != UserRole.ADMIN:
        raise errors.ForbiddenError(msg="The request is forbidden", msg_code=APIMsgCode.INVALID_REQUEST)
    return user

async def get_admin_or_operator(user: User = Depends(get_current_active_user)):
    if user.role not in [UserRole.ADMIN, UserRole.OPERATOR]:
        raise errors.ForbiddenError(msg="The request is forbidden", msg_code=APIMsgCode.INVALID_REQUEST)
    return user



class AuthServiceImpl(AuthService):
    def __init__(
            self,
            user_repository: UserRepo,
            otp_repo: OTPRecordRepo

    ):
        self.user_repository = user_repository
        self.otp_repo = otp_repo

    async def authenticate_user(self, email: str, password: str,
                                db: AsyncSession) -> TokenSch:
        user = await self.user_repository.get_by_email(email, db)
        if not user:
            raise errors.AuthorizationError(msg='Invalid email or password', msg_code=APIMsgCode.INVALID_CRED)
        if not verify_password(password, user.password):
            raise errors.AuthorizationError(msg='Invalid email or password', msg_code=APIMsgCode.INVALID_CRED)
        tokens = await create_tokens(user.id, user.email)
        return tokens

    async def refresh_tokens(self, refresh_token: str, db: AsyncSession) -> TokenSch:
        """Validate refresh token and create new token pair"""
        # Verify refresh token
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise errors.AuthorizationError(msg='Invalid refresh token')
        # Get user from payload
        user_id = int(payload.get("sub"))
        email = payload.get("email")
        # Create new tokens
        return await create_tokens(user_id, email)

    async def forgot_password(self, request: PasswordRecoveryRequest, db: AsyncSession,
                              background_tasks: BackgroundTasks) -> str:
        email = request.email.__str__()
        user = await self.user_repository.get_by_email(email, db)
        if not user:
            raise errors.NotFoundError(msg=f"No User found with email {email}")
        otp = self.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=2)

        await self.otp_repo.save_otp(email=request.email, otp=otp, expires_at=expires_at, db=db)
        background_tasks.add_task(self.send_otp_email, request.email, otp)
        return "OTP has been sent to your email."

    def generate_otp(self) -> str:
        return str(random.randint(100000, 999999))

    async def verify_otp(self, email: EmailStr, otp: str, db: AsyncSession) -> None:
        otp_record = await self.otp_repo.get_otp_record(email, db)
        if not otp_record:
            raise errors.NotFoundError(msg="OTP record not found for this email")
        if otp_record.otp != otp:
            raise errors.ConflictError(msg="Incorrect OTP")
        if otp_record.expires_at < datetime.utcnow():
            raise errors.ConflictError(msg="OTP has expired")

    async def reset_password(self, request: ResetPasswordRequest, db: AsyncSession) -> str:
        await self.verify_otp(request.email, request.otp, db)

        hashed_password = get_password_hash(request.new_password)
        await self.user_repository.update_password(email=request.email, new_password=hashed_password, db=db)
        return "Password reset successful"

    def send_otp_email(self, to_email: str, otp: str):
        subject = "Your OTP for Password Reset"
        sender_email = settings.SMTP_USER
        sender_name = settings.SMTP_SENDER_NAME

        html = f"""
        <html>
            <body>
                <p>Dear User,</p>
                <p>Your OTP for password reset is:</p>
                <h2>{otp}</h2>
                <p>This OTP is valid for 5 minutes.</p>
            </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{sender_name} <{sender_email}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.sendmail(sender_email, to_email, msg.as_string())
            print(f"OTP email sent to {to_email}")
        except smtplib.SMTPException as e:
            print(f"Failed to send OTP email to {to_email}: {str(e)}")
            raise errors.ConflictError(msg="Failed to send OTP email. Please try again later.")
