from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models.enum import PublishStatus, SortOrder
from src.app.models.student_assessment import StudentAssessment, StudentAssessmentSection, \
    StudentAssessmentQuestion, AssessmentInstitutionPublish
from src.app.repositories.base import BaseRepo
from src.app.schemas.student_assessment_sch import StudentAssessmentSortBy


class StudentAssessmentRepo(BaseRepo[StudentAssessment]):

    def __init__(self):
        super().__init__(StudentAssessment)

    async def get_with_details(self, assessment_id: int, db: AsyncSession) -> StudentAssessment | None:
        """Assessment with sections -> questions -> options and institution mappings (fixed number of queries)"""
        query = (
            select(StudentAssessment)
            .options(
                selectinload(StudentAssessment.sections)
                .selectinload(StudentAssessmentSection.questions)
                .selectinload(StudentAssessmentQuestion.options),
                selectinload(StudentAssessment.institution_mappings)
            )
            .where(StudentAssessment.id == assessment_id)
        )
        return await db.scalar(query)

    async def get_all_assessments(self, search: str | None, status: PublishStatus | None, course_id: int | None,
                                  sort_by: StudentAssessmentSortBy, sort_order: SortOrder,
                                  page: int, size: int, db: AsyncSession) -> tuple[list[StudentAssessment], int]:
        query = select(StudentAssessment)

        if status is not None:
            query = query.where(StudentAssessment.status == status)

        if course_id is not None:
            query = query.where(
                select(AssessmentInstitutionPublish.id)
                .where(
                    AssessmentInstitutionPublish.assessment_id == StudentAssessment.id,
                    AssessmentInstitutionPublish.course_id == course_id
                )
                .exists()
            )

        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    StudentAssessment.title.ilike(search_term),
                    StudentAssessment.instruction.ilike(search_term)
                )
            )

        total_elements = await db.scalar(select(func.count()).select_from(query.subquery()))
        if not total_elements:
            return [], 0

        sort_column = getattr(StudentAssessment, sort_by.value)
        order = sort_column.asc() if sort_order == SortOrder.ASC else sort_column.desc()

        # StudentAssessment.id as tie-breaker keeps page boundaries stable when sort values repeat
        query = (
            query
            .order_by(order, StudentAssessment.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await db.execute(query)
        return list(result.scalars().all()), total_elements
