from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.enum import SortOrder
from src.app.models.payment import Payment
from src.app.models.student import Student
from src.app.repositories.payment_repo import PaymentRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.repositories.user_repo import UserRepo
from src.app.schemas.payment_sch import CreatePaymentSch, GetPaymentSch, UpdatePaymentSch, PaymentSortBy
from src.app.services.payment_service import PaymentService
from src.app.models.user import User
from src.app.shared.response import PaginationResponse
from src.app.utils.institution_scope import resolve_institution_id



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
        student = await self.student_repo.get(sch.student_id, db)
        if not student:
            raise errors.HTTPError(code=404, msg=f"Student not found with id: {sch.student_id}")

        new_payment = Payment(
            amount_paid=sch.amount_paid,
            payment_date=sch.payment_date,
            payment_mode=sch.payment_mode,
            remarks=sch.remarks,
            student_id=sch.student_id,
        )
        self._apply_amount(student, sch.amount_paid)

        # single commit persists the payment and the student's updated balance together
        payment = await self.payment_repo.save(new_payment, db)
        return payment.id

    async def get_payment_by_id(self, payment_id: int, db: AsyncSession) -> GetPaymentSch:
        payment = await self.payment_repo.get(payment_id, db)
        if not payment:
            raise errors.HTTPError(code=404, msg=f"Payment with id {payment_id} not found!")

        return GetPaymentSch.from_entity(payment)

    async def get_all_payments(self, user: User, search: str | None, institution_id: int | None,
                               student_id: int | None,
                               sort_by: PaymentSortBy, sort_order: SortOrder,
                               page: int, size: int, db: AsyncSession) -> PaginationResponse[GetPaymentSch]:
        # operator always gets own institution payments, admin gets all or the selected institution
        institution_id = resolve_institution_id(user, institution_id)
        payments, total_elements = await self.payment_repo.get_all_payments(
            search, institution_id, student_id, sort_by, sort_order, page, size, db)

        payment_list = [GetPaymentSch.from_entity(payment) for payment in payments]

        return PaginationResponse[GetPaymentSch](body=payment_list).set_page_info(
            total_elements=total_elements, page=page, size=size)

    async def update_payment(self, sch: UpdatePaymentSch, db: AsyncSession) -> str:
        payment = await self.payment_repo.get(sch.id, db)
        if not payment:
            raise errors.HTTPError(code=404, msg=f"Payment with id {sch.id} not found!")

        new_student = await self.student_repo.get(sch.student_id, db)
        if not new_student:
            raise errors.HTTPError(code=404, msg=f"Student not found with id: {sch.student_id}")

        old_student = (new_student if payment.student_id == sch.student_id
                       else await self.student_repo.get(payment.student_id, db))

        # reverse the old amount, then apply the new one (handles both amount and student changes)
        self._apply_amount(old_student, -payment.amount_paid)
        self._apply_amount(new_student, sch.amount_paid)

        payment.student_id = sch.student_id
        payment.amount_paid = sch.amount_paid
        payment.payment_date = sch.payment_date
        payment.payment_mode = sch.payment_mode
        payment.remarks = sch.remarks
        await self.payment_repo.save(payment, db)
        return "Payment updated successfully"

    async def delete_payment(self, payment_id: int, db: AsyncSession) -> str:
        payment = await self.payment_repo.get(payment_id, db)
        if not payment:
            raise errors.HTTPError(code=404, msg=f"Payment with id {payment_id} not found!")

        student = await self.student_repo.get(payment.student_id, db)
        self._apply_amount(student, -payment.amount_paid)

        # single commit removes the payment and saves the student's reverted balance together
        await self.payment_repo.delete(payment, db)
        return "Payment deleted successfully"

    @staticmethod
    def _apply_amount(student: Student, amount: float) -> None:
        """Add (or, when negative, reverse) a payment amount and recompute balance and status"""
        student.paid_amount = max(student.paid_amount + amount, 0)
        student.refresh_payment_status()
