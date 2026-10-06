from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_payment_service
from src.app.models.enum import SortOrder
from src.app.models.user import User
from src.app.schemas.payment_sch import CreatePaymentSch, GetPaymentSch, UpdatePaymentSch, PaymentSortBy
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.payment_service import PaymentService
from src.app.shared.response import Response, PaginationResponse

payment_router = APIRouter()


@payment_router.post("", response_model=Response[int], name="Create payment")
async def create_payment(sch: CreatePaymentSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: PaymentService = Depends(get_payment_service)):
    return Response[int](body=await service.create_payment(sch, session))

@payment_router.put("", response_model=Response[str], name="Update payment")
async def update_payment(sch: UpdatePaymentSch, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: PaymentService = Depends(get_payment_service)):
    return Response[str](body=await service.update_payment(sch, session))

@payment_router.get("/get_all_payments", response_model=PaginationResponse[GetPaymentSch],
                    name="Get all Payments")
async def get_all_payments(search: str | None = None,
                           student_id: int | None = None,
                           sort_by: PaymentSortBy = PaymentSortBy.ID,
                           sort_order: SortOrder = SortOrder.DESC,
                           page: int = Query(1, ge=1),
                           size: int = Query(10, ge=1, le=100),
                           session: AsyncSession = Depends(get_db),
                           user: User = Depends(get_admin_or_operator),
                           service: PaymentService = Depends(get_payment_service)):
    return await service.get_all_payments(search, student_id, sort_by, sort_order, page, size, session)

@payment_router.get("/{payment_id}", response_model=Response[GetPaymentSch], name="Get Payment Details By ID")
async def get_payment_by_id(payment_id: int, session: AsyncSession = Depends(get_db),
                            user: User = Depends(get_admin_or_operator),
                            service: PaymentService = Depends(get_payment_service)):
    return Response[GetPaymentSch](body=await service.get_payment_by_id(payment_id, session))

@payment_router.delete("/{payment_id}", response_model=Response[str], name="Delete payment")
async def delete_payment(payment_id: int, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin_or_operator),
                         service: PaymentService = Depends(get_payment_service)):
    return Response[str](body=await service.delete_payment(payment_id, session))
