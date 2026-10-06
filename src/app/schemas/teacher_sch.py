from pydantic import EmailStr, BaseModel
from src.app.models.user import User
from src.app.schemas.institution_sch import InstitutionDropDown


class CreateTeacherSch(BaseModel):
    name: str
    email: EmailStr
    password:str
    phone_number:str
    address:str
    institution_id: int

class UpdateTeacherSch(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str
    institution_id: int

class GetTeacherDetailsSch(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    role: str
    institution: InstitutionDropDown | None = None

    @staticmethod
    def from_entity(teacher: User) -> 'GetTeacherDetailsSch':

        return GetTeacherDetailsSch(
            id=teacher.id,
            name=teacher.name,
            email=teacher.email,
            phone_number=teacher.phone_number,
            address=teacher.address,
            role=teacher.role,
            institution=(
                InstitutionDropDown.from_entity(teacher.institution)
                if teacher.institution else None
            )
        )