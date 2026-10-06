import enum
from pydantic import EmailStr, BaseModel

from src.app.models.user import User
from src.app.schemas.institution_sch import InstitutionDropDown


class OperatorSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"

class CreateOperatorSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str
    institution_id: int

class UpdateOperatorSch(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str
    institution_id: int

class GetOperatorSch(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    role: str
    institution: InstitutionDropDown | None = None

    @staticmethod
    def from_entity(operator: User) -> 'GetOperatorSch':
        return GetOperatorSch(
            id=operator.id,
            name=operator.name,
            email=operator.email,
            phone_number=operator.phone_number,
            address=operator.address,
            role=operator.role,
            institution=(
                InstitutionDropDown.from_entity(operator.institution)
                if operator.institution else None
            )
        )
