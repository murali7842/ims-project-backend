from pydantic import EmailStr
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import OTPRecord
from src.app.repositories.base import BaseRepo


class OTPRecordRepo(BaseRepo[OTPRecord]):

    def __init__(self):
        super().__init__(OTPRecord)

    async def save_otp(self, email: EmailStr, otp: str, expires_at, db: AsyncSession):
        await db.execute(delete(OTPRecord).where(OTPRecord.email == email))  # Remove old OTP
        db.add(OTPRecord(email=email, otp=otp, expires_at=expires_at))
        await db.commit()

    async def get_otp_record(self, email: EmailStr, db: AsyncSession) -> OTPRecord | None:
        result = await db.execute(select(OTPRecord).where(OTPRecord.email == email))
        return result.scalar_one_or_none()
