import enum
from pydantic import EmailStr, BaseModel

from src.app.models.enum import UserRole
from src.app.models.user import User
from src.app.schemas.institution_sch import InstitutionDropDown


class UserSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"

class UserRegSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str

class UpdateUserSch(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str

class GetUserSch(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    role: UserRole
    institution: InstitutionDropDown | None = None

    @staticmethod
    def from_entity(user: User) -> "GetUserSch":
        return GetUserSch(
            id=user.id,
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            address=user.address,
            role=user.role,
            institution=(
                InstitutionDropDown.from_entity(user.institution)
                if user.institution else None
            )
        )
