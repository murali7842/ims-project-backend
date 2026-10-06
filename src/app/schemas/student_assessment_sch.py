import enum
from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from src.app.models.enum import PublishStatus, QuestionType, ResponseStatus
from src.app.models.student_assessment import StudentAssessment, StudentAssessmentSection, \
    StudentAssessmentQuestion, StudentAssessmentQuestionOption


class StudentAssessmentSortBy(str, enum.Enum):
    ID = "id"
    TITLE = "title"
    START_DATE = "start_date"
    END_DATE = "end_date"

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

class StudentAssessmentUpdateSch(StudentAssessmentCreateSch):
    """
    id is required here. For section / questions / options: items with an id are updated,
    items without an id are created, and existing items left out of the list are removed.
    section=None leaves sections untouched; institution_ids=None leaves mappings untouched.
    """
    id: int

class StudentAssessmentAnswerCreateSch(BaseModel):
    question_id: int
    option_answer: list[int] | None = None
    answer: str | None = None
    answer_attachment: str | None = None

class StudentAssessmentAttemptCreateSch(BaseModel):
    student_id: int
    student_assessment_id: int
    answers: list[StudentAssessmentAnswerCreateSch]


class QuestionOptionSch(BaseModel):
    id: int
    option: str | None
    option_attachment: dict | None
    is_correct: bool | None

    @staticmethod
    def from_entity(option: StudentAssessmentQuestionOption) -> "QuestionOptionSch":
        return QuestionOptionSch(
            id=option.id,
            option=option.option,
            option_attachment=option.option_attachment,
            is_correct=option.is_correct
        )

class QuestionSch(BaseModel):
    id: int
    question_text: str
    question_type: QuestionType
    required: bool | None
    min_range: int | None
    max_range: int | None
    min_label: str | None
    max_label: str | None
    correct_answer: Any | None
    question_attachment: dict | None
    options: list[QuestionOptionSch]

    @staticmethod
    def from_entity(question: StudentAssessmentQuestion) -> "QuestionSch":
        return QuestionSch(
            id=question.id,
            question_text=question.question_text,
            question_type=question.question_type,
            required=question.required,
            min_range=question.min_range,
            max_range=question.max_range,
            min_label=question.min_label,
            max_label=question.max_label,
            correct_answer=question.correct_answer,
            question_attachment=question.question_attachment,
            options=[QuestionOptionSch.from_entity(option) for option in question.options]
        )

class SectionSch(BaseModel):
    id: int
    name: str
    questions: list[QuestionSch]

    @staticmethod
    def from_entity(section: StudentAssessmentSection) -> "SectionSch":
        return SectionSch(
            id=section.id,
            name=section.name,
            questions=[QuestionSch.from_entity(question) for question in section.questions]
        )

class StudentAssessmentSch(BaseModel):
    """List item: assessment details without the question tree"""
    id: int
    title: str
    instruction: str | None
    status: PublishStatus
    start_date: date | None
    end_date: date | None
    passing_marks: float | None

    @staticmethod
    def from_entity(assessment: StudentAssessment) -> "StudentAssessmentSch":
        return StudentAssessmentSch(
            id=assessment.id,
            title=assessment.title,
            instruction=assessment.instruction,
            status=assessment.status,
            start_date=assessment.start_date,
            end_date=assessment.end_date,
            passing_marks=assessment.passing_marks
        )

class StudentAssessmentDetailSch(StudentAssessmentSch):
    course_id: int | None
    institution_ids: list[int]
    sections: list[SectionSch]

    @staticmethod
    def from_entity(assessment: StudentAssessment) -> "StudentAssessmentDetailSch":
        mappings = assessment.institution_mappings
        return StudentAssessmentDetailSch(
            **StudentAssessmentSch.from_entity(assessment).model_dump(),
            course_id=mappings[0].course_id if mappings else None,
            institution_ids=[mapping.institution_id for mapping in mappings],
            sections=[SectionSch.from_entity(section) for section in assessment.sections]
        )
