from pydantic import BaseModel, EmailStr, Field


class TokenSch(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str

class PasswordRecoveryRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str = Field(min_length=6)