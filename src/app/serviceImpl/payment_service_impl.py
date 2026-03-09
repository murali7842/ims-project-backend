from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.enum import PaymentStatus
from src.app.models.payment import Payment
from src.app.models.student import Student
from src.app.repositories.payment_repo import PaymentRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.payment_sch import CreatePaymentSch
from src.app.services.payment_service import PaymentService



class PaymentServiceImpl(PaymentService):

    def __init__(self,
                 payment_repo: PaymentRepo,
                 user_repo: UserRepo,
                 student_repo: StudentRepo
                 ):
        super().__init__()
        self.payment_repo = payment_repo
        self.user_repo =  user_repo
        self.student_repo = student_repo

    async def create_payment(self, sch: CreatePaymentSch, db: AsyncSession) -> int:
        # 1️⃣ Fetch the student
        student = await self.student_repo.get(sch.student_id, db)
        if not student:
            raise errors.HTTPError(code=400, msg=f"Student not found with id: {sch.student_id}")

        # 2️⃣ Create new payment record
        new_payment = Payment(
            amount_paid=sch.amount_paid,
            payment_date=sch.payment_date,
            payment_mode=sch.payment_mode,
            remarks=sch.remarks,
            student_id=sch.student_id,
        )
        payment = await self.payment_repo.save(new_payment, db)

        # 3️⃣ Update student's paid amount & balance
        student.paid_amount += sch.amount_paid
        student.balance_amount = max(student.fee_amount - student.paid_amount, 0)  # no negatives

        # 4️⃣ Update payment status
        if student.paid_amount == 0:
            student.payment_status = PaymentStatus.UNPAID
        elif student.paid_amount < student.fee_amount:
            student.payment_status = PaymentStatus.PARTIALLY_PAID
        else:
            student.payment_status = PaymentStatus.PAID

        # 5️⃣ Save updated student record
        await self.student_repo.save(student, db)
        return payment.id