from pydantic import EmailStr, BaseModel

from src.app.models.enum import UserRole


class UserRegSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str
