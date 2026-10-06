from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_user_service
from src.app.models.enum import UserRole, SortOrder
from src.app.models.user import User
from src.app.schemas.user_sch import UserRegSch, GetUserSch, UpdateUserSch, UserSortBy
from src.app.serviceImpl.auth_service_impl import get_admin
from src.app.services.user_service import UserService
from src.app.shared.response import Response, PaginationResponse

user_router = APIRouter()


@user_router.post("/register", response_model=Response[int], name="User Registration")
async def reg_user(sch: UserRegSch, session: AsyncSession = Depends(get_db), service: UserService = Depends(get_user_service)):
    return Response[int](body=await service.reg_user(sch, session))

@user_router.put("", response_model=Response[str], name="Update User")
async def update_user(sch: UpdateUserSch, session: AsyncSession = Depends(get_db),
                      user: User = Depends(get_admin),
                      service: UserService = Depends(get_user_service)):
    return Response[str](body=await service.update_user(sch, session))

@user_router.get("/get_all_users", response_model=PaginationResponse[GetUserSch], name="Get all Users")
async def get_all_users(search: str | None = None,
                        role: UserRole | None = None,
                        sort_by: UserSortBy = UserSortBy.ID,
                        sort_order: SortOrder = SortOrder.DESC,
                        page: int = Query(1, ge=1),
                        size: int = Query(10, ge=1, le=100),
                        session: AsyncSession = Depends(get_db),
                        user: User = Depends(get_admin),
                        service: UserService = Depends(get_user_service)):
    return await service.get_all_users(search, role, sort_by, sort_order, page, size, session)

@user_router.get("/{user_id}", response_model=Response[GetUserSch], name="Get User Details By ID")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db),
                         user: User = Depends(get_admin),
                         service: UserService = Depends(get_user_service)):
    return Response[GetUserSch](body=await service.get_user_by_id(user_id, session))

@user_router.delete("/{user_id}", response_model=Response[str], name="Delete User")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db),
                      user: User = Depends(get_admin),
                      service: UserService = Depends(get_user_service)):
    return Response[str](body=await service.delete_user(user_id, user.id, session))
