from datetime import date

from sqlalchemy import String, ForeignKey, Boolean, Enum as SQLAlchemyEnum, JSON, Date, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.config.db_config import Base
from src.app.models.base import Auditable
from src.app.models.enum import QuestionType, ResponseStatus, PublishStatus, AttemptStatus


class StudentAssessment(Base, Auditable):
    __tablename__ = "student_assessment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    instruction: Mapped[str] = mapped_column(String(2000), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    status: Mapped[PublishStatus] = mapped_column(
        SQLAlchemyEnum(PublishStatus, native_enum=False, length=20)
    )
    passing_marks: Mapped[float | None] = mapped_column(Float, nullable=True)
    sections: Mapped[list["StudentAssessmentSection"]] = relationship(
        "StudentAssessmentSection", back_populates="student_assessment", cascade="all, delete-orphan"
    )
    attempts: Mapped[list["StudentAssessmentAttempt"]] = relationship(
        "StudentAssessmentAttempt", back_populates="student_assessment", cascade="all, delete-orphan"
    )
    institution_mappings: Mapped[list["AssessmentInstitutionPublish"]] = relationship(
        "AssessmentInstitutionPublish", back_populates="assessment"
    )

class StudentAssessmentSection(Base, Auditable):
    __tablename__ = "student_assessment_section"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    student_assessment_id: Mapped[int] = mapped_column(ForeignKey("student_assessment.id", ondelete="CASCADE"))
    student_assessment: Mapped["StudentAssessment"] = relationship("StudentAssessment", back_populates="sections")
    questions: Mapped[list["StudentAssessmentQuestion"]] = relationship(
        "StudentAssessmentQuestion", back_populates="section", cascade="all, delete-orphan"
    )

class StudentAssessmentQuestion(Base, Auditable):
    __tablename__ = "student_assessment_question"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_text: Mapped[str] = mapped_column(String(1000))
    question_type: Mapped[QuestionType] = mapped_column(SQLAlchemyEnum(QuestionType), nullable=False)
    required: Mapped[bool] = mapped_column(Boolean)
    min_range: Mapped[int | None] = mapped_column(Integer)
    max_range: Mapped[int | None] = mapped_column(Integer)
    min_label: Mapped[str | None] = mapped_column(String(100))
    max_label: Mapped[str | None] = mapped_column(String(100))
    section_id: Mapped[int] = mapped_column(ForeignKey("student_assessment_section.id"), index=True)
    correct_answer: Mapped[JSON] = mapped_column(JSON, nullable=True)
    question_attachment: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    section: Mapped["StudentAssessmentSection"] = relationship("StudentAssessmentSection", back_populates="questions")
    options: Mapped[list["StudentAssessmentQuestionOption"]] = relationship(
        "StudentAssessmentQuestionOption", back_populates="question", cascade="all, delete-orphan"
    )
    answers: Mapped[list["StudentAssessmentAnswer"]] = relationship("StudentAssessmentAnswer", back_populates="question")


class StudentAssessmentQuestionOption(Base, Auditable):
    __tablename__ = "student_assessment_question_option"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    option: Mapped[str | None] = mapped_column(String(255), nullable=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("student_assessment_question.id", ondelete="CASCADE"))
    option_attachment: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    question: Mapped["StudentAssessmentQuestion"] = relationship("StudentAssessmentQuestion", back_populates="options")


class AssessmentInstitutionPublish(Base, Auditable):
    __tablename__ = "assessment_institution_publish"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("student_assessment.id", ondelete="CASCADE"), nullable=False,
                                               index=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id", ondelete="CASCADE"), nullable=False,
                                                index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), nullable=False, index=True)

    # Fix relationship names and add proper back_populates
    assessment: Mapped["StudentAssessment"] = relationship(
        "StudentAssessment", back_populates="institution_mappings"
    )
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="assessment_publishes"  # This should match Institution model
    )
    course: Mapped["Course"] = relationship("Course")


class StudentAssessmentAttempt(Base, Auditable):
    __tablename__ = "student_assessment_attempt"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_assessment_id: Mapped[int] = mapped_column(ForeignKey("student_assessment.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    marks: Mapped[int] = mapped_column(Integer)
    auto_graded: Mapped[bool] = mapped_column(Boolean, default=False)
    total_marks: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[AttemptStatus] = mapped_column(
        SQLAlchemyEnum(AttemptStatus, native_enum=False, length=20),
        default=AttemptStatus.SUBMITTED
    )
    grade: Mapped[str | None] = mapped_column(String(10), nullable=True)

    student_assessment: Mapped["StudentAssessment"] = relationship("StudentAssessment", back_populates="attempts")
    student: Mapped["Student"] = relationship("Student", back_populates="attempts")
    answers: Mapped[list["StudentAssessmentAnswer"]] = relationship(
        "StudentAssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan"
    )


class StudentAssessmentAnswer(Base, Auditable):
    __tablename__ = "student_assessment_answer"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("student_assessment_attempt.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("student_assessment_question.id", ondelete="CASCADE"))
    option_answer: Mapped[list[int]] = mapped_column(JSON)
    answer: Mapped[str | None] = mapped_column(Text)
    answer_attachment: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    response: Mapped[ResponseStatus] = mapped_column(SQLAlchemyEnum(ResponseStatus,
                                                                    name="response_status", create_type=False))

    attempt: Mapped["StudentAssessmentAttempt"] = relationship("StudentAssessmentAttempt", back_populates="answers")
    question: Mapped["StudentAssessmentQuestion"] = relationship("StudentAssessmentQuestion", back_populates="answers")
