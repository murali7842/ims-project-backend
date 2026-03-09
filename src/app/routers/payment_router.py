from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_payment_service
from src.app.models.user import User
from src.app.schemas.payment_sch import CreatePaymentSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.payment_service import PaymentService
from src.app.shared.response import Response

payment_router = APIRouter()


@payment_router.post("", response_model=Response[int], name="Create payment")
async def create_payment(sch: CreatePaymentSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: PaymentService = Depends(get_payment_service)):
    return Response[int](body=await service.create_payment(sch, session))