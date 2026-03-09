from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.exception import errors
from src.app.models.enum import AttemptStatus, ResponseStatus
from src.app.models.student_assessment import StudentAssessment, StudentAssessmentSection, StudentAssessmentQuestion, \
    StudentAssessmentQuestionOption, AssessmentInstitutionPublish, StudentAssessmentAnswer, StudentAssessmentAttempt
from src.app.repositories.assessment_institution_publish_repo import AssessmentInstitutionPublishRepo
from src.app.repositories.institution_repo import InstitutionRepo
from src.app.repositories.student_assessment_attempt_repo import StudentAssessmentAttemptRepo
from src.app.repositories.student_assessment_question_option_repo import StudentAssessmentQuestionOptionRepo
from src.app.repositories.student_assessment_question_repo import StudentAssessmentQuestionRepo
from src.app.repositories.student_assessment_repo import StudentAssessmentRepo
from src.app.repositories.student_repo import StudentRepo
from src.app.schemas.student_assessment_sch import StudentAssessmentCreateSch, StudentAssessmentAttemptCreateSch
from src.app.services.student_assessment_service import StudentAssessmentService
from src.app.utils import upload_util


class StudentAssessmentServiceImpl(StudentAssessmentService):
    def __init__(self,
                 student_assessment_repo: StudentAssessmentRepo,
                 student_assessment_question_repo: StudentAssessmentQuestionRepo,
                 student_assessment_question_option_repo: StudentAssessmentQuestionOptionRepo,
                 assessment_institution_publish_repo: AssessmentInstitutionPublishRepo,
                 institution_repo: InstitutionRepo,
                 student_assessment_attempt_repo: StudentAssessmentAttemptRepo,
                 # student_repo: StudentRepo

                 ):
        super().__init__()
        self.student_assessment_repo = student_assessment_repo
        self.student_assessment_question_repo = student_assessment_question_repo
        self.student_assessment_question_option_repo = student_assessment_question_option_repo
        self.assessment_institution_publish_repo = assessment_institution_publish_repo
        self.institution_repo = institution_repo
        self.student_assessment_attempt_repo = student_assessment_attempt_repo
        # self.student_repo =student_repo
        self.attachment_id_counter = 1

    async def create_assessment(self, sch: StudentAssessmentCreateSch, db: AsyncSession) -> str:
        assessment = StudentAssessment(
            title=sch.title,
            instruction=sch.instruction,
            status=sch.status,
            passing_marks=sch.passing_marks,
            start_date=sch.start_date,
            end_date=sch.end_date,
        )

        if sch.section:
            for section_data in sch.section:
                section = StudentAssessmentSection(name=section_data.name)
                section.student_assessment = assessment

                for question_data in section_data.questions:
                    # Initialize attachment dict
                    question = StudentAssessmentQuestion(
                        question_text=question_data.question_text,
                        question_type=question_data.question_type,
                        min_range=question_data.min_range,
                        max_range=question_data.max_range,
                        min_label=question_data.min_label,
                        max_label=question_data.max_label,
                        required=question_data.required,
                        correct_answer=question_data.correct_answer,
                        question_attachment={}
                    )

                    # Process single base64 string for question attachment
                    if question_data.question_attachment:
                        attachment_info = await self.process_attachment_file(question_data.question_attachment)
                        if attachment_info:
                            question.question_attachment = attachment_info

                    # Handle options
                    for option_data in question_data.options or []:
                        option = StudentAssessmentQuestionOption(
                            option=option_data.option,
                            option_attachment={}
                        )

                        if option_data.option_attachment:
                            opt_attach_info = await self.process_attachment_file(option_data.option_attachment)
                            if opt_attach_info:
                                option.option_attachment = opt_attach_info

                        option.question = question
                        question.options.append(option)

                    question.section = section
                    section.questions.append(question)

                assessment.sections.append(section)

        saved_assessment = await self.student_assessment_repo.save(assessment, db)
        if sch.institution_ids:
            institutions = await self.institution_repo.get_multiple(sch.institution_ids, db)
            if len(institutions) != len(sch.institution_ids):
                raise errors.HTTPError(code=404, msg="One or more school IDs are invalid")

            associations = [
                AssessmentInstitutionPublish(
                    assessment_id=saved_assessment.id,
                    institution_id=institution_id,
                    course_id=sch.course_id
                )
                for institution_id in sch.institution_ids
            ]
            await self.assessment_institution_publish_repo.save_all(associations, db)

        return f"Assessment with ID:{saved_assessment.id} is saved successfully"

    async def process_attachment_file(self, base64_file: str) -> str:
        loc = "/assessment/attachments/"
        file_info = await upload_util.save_base64_to_file(base64_file, Path(loc))
        # file_info["uuid"] = uuid.uuid4().int
        file_info["id"] = self.attachment_id_counter
        self.attachment_id_counter += 1
        return file_info

    async def create_attempt(
        self,
        sch: StudentAssessmentAttemptCreateSch,
        db: AsyncSession
    ) -> str:
        # Check if already attempted with student id
        attempted = await self.student_assessment_attempt_repo.check_attempted_assessment(
            student_id=sch.student_id,
            assessment_id=sch.student_assessment_id,
            db=db
        )
        if attempted:
            raise errors.HTTPError(code=400, msg="Assessment already attempted by this student.")

        # Fetch assessment details for passing marks
        assessment = await db.get(StudentAssessment, sch.student_assessment_id)
        if not assessment:
            raise errors.HTTPError(code=404, msg=f"Assessment not found with ID {sch.student_assessment_id}")

        # Create attempt entry
        attempt = StudentAssessmentAttempt(
            student_id=sch.student_id,
            student_assessment_id=sch.student_assessment_id,
        )

        total_questions = len(sch.answers)
        correct_count = 0

        # Evaluate each question
        for ans_data in sch.answers:
            # Get question and correct answer
            question = await db.get(StudentAssessmentQuestion, ans_data.question_id)
            if not question:
                raise errors.HTTPError(code=404, msg=f"Question not found with ID {ans_data.question_id}")

            is_correct = False

            # --- CASE 1: If correct_answer is numeric or list (MCQ) ---
            if question.correct_answer:
                def normalize(value):
                    if value is None:
                        return []
                    if isinstance(value, list):
                        return [str(v).strip() for v in value]
                    if isinstance(value, str):
                        return [v.strip() for v in value.split(",") if v.strip()]
                    if isinstance(value, (int, float)):
                        return [str(int(value))]
                    return []

                user_ans = normalize(ans_data.option_answer)
                correct_ans = normalize(question.correct_answer)

                if sorted(user_ans) == sorted(correct_ans):
                    is_correct = True

                # --- CASE 2: Text-based answers ---
                elif ans_data.answer and isinstance(question.correct_answer, str):
                    if ans_data.answer.strip().lower() == question.correct_answer.strip().lower():
                        is_correct = True

            response = ResponseStatus.CORRECT if is_correct else ResponseStatus.IN_CORRECT
            if is_correct:
                correct_count += 1

            # Create answer record
            answer_attachment_data = {}
            if ans_data.answer_attachment:
                answer_attachment_data = await self.process_attachment_file(ans_data.answer_attachment)

            answer = StudentAssessmentAnswer(
                question_id=ans_data.question_id,
                option_answer=ans_data.option_answer,
                answer=ans_data.answer,
                answer_attachment=answer_attachment_data,
                response=response
            )
            answer.attempt = attempt
            attempt.answers.append(answer)

        # Calculate results
        total_marks = total_questions
        score = correct_count
        percentage = int((score / total_marks) * 100) if total_marks > 0 else 0

        passing_marks = assessment.passing_marks or 0
        pass_fail = "PASS" if percentage >= passing_marks else "FAIL"

        # Set final attempt details
        attempt.marks = score
        attempt.total_marks = total_marks
        attempt.overall_score = percentage
        attempt.status = AttemptStatus.SUBMITTED
        attempt.grade = pass_fail

        # Save in DB
        saved_attempt = await self.student_assessment_attempt_repo.save(attempt, db)

        # Return summary
        return (
            f"Assessment {assessment.title} completed by Student ID {sch.student_id}. "
            f"Score: {score}/{total_marks} ({percentage}%). Result: {pass_fail}. "
            f"Attempt ID: {saved_attempt.id}"
        )
