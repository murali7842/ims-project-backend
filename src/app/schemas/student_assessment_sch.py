from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from src.app.models.enum import PublishStatus, QuestionType, ResponseStatus


class QuestionOptionCreateSch(BaseModel):
    id :int |None =None
    option: str | None = None
    option_attachment: str | None = None

class QuestionCreateSch(BaseModel):
    id:int | None =None
    question_text: str
    question_type: QuestionType
    min_range: int | None = None
    max_range: int | None = None
    min_label: str | None = None
    max_label: str | None = None
    required: bool | None = False
    correct_answer: Any   | None = None
    question_attachment: str | None = None
    options: list[QuestionOptionCreateSch] = Field(default_factory=list)

class SectionCreateSch(BaseModel):
    id: int | None= None
    name: str
    questions: list[QuestionCreateSch]

class StudentAssessmentCreateSch(BaseModel):
    id:int | None = None
    title: str
    instruction: str | None = None
    status: PublishStatus
    start_date: date | None = None
    end_date: date | None = None
    passing_marks: float | None = None
    course_id: int
    section: list[SectionCreateSch] | None = None
    institution_ids: list[int] | None = None

class StudentAssessmentAnswerCreateSch(BaseModel):
    question_id: int
    option_answer: list[int] | None = None
    answer: str | None = None
    answer_attachment: str | None = None

class StudentAssessmentAttemptCreateSch(BaseModel):
    student_id: int
    student_assessment_id: int
    answers: list[StudentAssessmentAnswerCreateSch]
