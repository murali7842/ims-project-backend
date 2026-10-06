from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_student_assessment_service
from src.app.models.enum import PublishStatus, SortOrder
from src.app.schemas.student_assessment_sch import StudentAssessmentCreateSch, StudentAssessmentAttemptCreateSch, \
    StudentAssessmentUpdateSch, StudentAssessmentSch, StudentAssessmentDetailSch, StudentAssessmentSortBy
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.student_assessment_service import StudentAssessmentService
from src.app.shared.response import Response, PaginationResponse
from src.app.models.user import User

student_assessment_router = APIRouter()


@student_assessment_router.post("", response_model=Response[str], name="Create Student Assessment")
async def create_student_assessment(
        sch: StudentAssessmentCreateSch,
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return Response[str](body=await service.create_assessment(sch, db))

@student_assessment_router.post("/attempt", response_model=Response[str],
                                name="Create Student Assessment Attempt")
async def create_student_assessment_attempt(
        sch: StudentAssessmentAttemptCreateSch,
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return Response[str](body=await service.create_attempt(sch, db))

@student_assessment_router.put("", response_model=Response[str], name="Update Student Assessment")
async def update_student_assessment(
        sch: StudentAssessmentUpdateSch,
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return Response[str](body=await service.update_assessment(sch, db))

@student_assessment_router.get("/get_all_assessments", response_model=PaginationResponse[StudentAssessmentSch],
                               name="Get all Student Assessments")
async def get_all_student_assessments(
        search: str | None = None,
        status: PublishStatus | None = None,
        course_id: int | None = None,
        sort_by: StudentAssessmentSortBy = StudentAssessmentSortBy.ID,
        sort_order: SortOrder = SortOrder.DESC,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return await service.get_all_assessments(search, status, course_id, sort_by, sort_order, page, size, db)

@student_assessment_router.get("/{assessment_id}", response_model=Response[StudentAssessmentDetailSch],
                               name="Get Student Assessment Details By ID")
async def get_student_assessment_by_id(
        assessment_id: int,
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return Response[StudentAssessmentDetailSch](body=await service.get_assessment_by_id(assessment_id, db))

@student_assessment_router.delete("/{assessment_id}", response_model=Response[str],
                                  name="Delete Student Assessment")
async def delete_student_assessment(
        assessment_id: int,
        user: User = Depends(get_admin_or_operator),
        db: AsyncSession = Depends(get_db),
        service: StudentAssessmentService = Depends(get_student_assessment_service)
):
    return Response[str](body=await service.delete_assessment(assessment_id, db))
