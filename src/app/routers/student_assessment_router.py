from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dependencies.db import get_db
from src.app.dependencies.service import get_student_assessment_service
from src.app.schemas.student_assessment_sch import StudentAssessmentCreateSch, StudentAssessmentAttemptCreateSch
from src.app.serviceImpl.auth_service_impl import get_admin_or_operator
from src.app.services.student_assessment_service import StudentAssessmentService
from src.app.shared.response import Response
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
