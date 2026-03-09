from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.student_assessment_sch import StudentAssessmentCreateSch, StudentAssessmentAttemptCreateSch


class StudentAssessmentService(ABC):

    @abstractmethod
    async def create_assessment(self, sch: StudentAssessmentCreateSch, db: AsyncSession) -> str:
        pass

    @abstractmethod
    async def create_attempt(self, sch: StudentAssessmentAttemptCreateSch, db: AsyncSession) -> str:
        pass