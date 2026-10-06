import enum
from pydantic import BaseModel, EmailStr
from src.app.models.enum import StudentStatus, PaymentStatus
from src.app.models.student import Student


class StudentSortBy(str, enum.Enum):
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    BALANCE_AMOUNT = "balance_amount"

class CreateStudentSch(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str
    guardian_name: str
    guardian_phone: str
    status : StudentStatus
    institution_id: int
    course_id: int
    batch_id: int

class UpdateStudentSch(CreateStudentSch):
    id: int

class GetStudentSch(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    address: str
    guardian_name: str | None
    guardian_phone: str | None
    fee_amount: float
    paid_amount: float
    balance_amount: float
    payment_status: PaymentStatus
    status: StudentStatus
    institution_id: int
    course_id: int
    batch_id: int

    @staticmethod
    def from_entity(student: Student) -> "GetStudentSch":
        return GetStudentSch(
            id=student.id,
            name=student.name,
            email=student.email,
            phone_number=student.phone_number,
            address=student.address,
            guardian_name=student.guardian_name,
            guardian_phone=student.guardian_phone,
            fee_amount=student.fee_amount,
            paid_amount=student.paid_amount,
            balance_amount=student.balance_amount,
            payment_status=student.payment_status,
            status=student.status,
            institution_id=student.institution_id,
            course_id=student.course_id,
            batch_id=student.batch_id
        )
