from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.enum import PublishStatus, SortOrder
from src.app.schemas.student_assessment_sch import StudentAssessmentCreateSch, StudentAssessmentAttemptCreateSch, \
    StudentAssessmentUpdateSch, StudentAssessmentSch, StudentAssessmentDetailSch, StudentAssessmentSortBy
from src.app.shared.response import PaginationResponse


class StudentAssessmentService(ABC):

    @abstractmethod
    async def create_assessment(self, sch: StudentAssessmentCreateSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def create_attempt(self, sch: StudentAssessmentAttemptCreateSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def get_all_assessments(self, search: str | None, status: PublishStatus | None, course_id: int | None,
                                  sort_by: StudentAssessmentSortBy, sort_order: SortOrder,
                                  page: int, size: int, db: AsyncSession) -> PaginationResponse[StudentAssessmentSch]:
        pass

    @abstractmethod
    async def get_assessment_by_id(self, assessment_id: int, db: AsyncSession) -> StudentAssessmentDetailSch:
        pass

    @abstractmethod
    async def update_assessment(self, sch: StudentAssessmentUpdateSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def delete_assessment(self, assessment_id: int, db: AsyncSession) -> str:
        pass
