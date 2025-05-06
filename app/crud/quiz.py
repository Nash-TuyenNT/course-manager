from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.models.quiz_models import LessonQuiz, QuizQuestion
from app.models.quiz_models import StudentQuizResult
from app.models.user import User
from app.models.user_lesson_progress import UserLessonProgress
from app.schemas.quiz import QuizCreate, QuizUpdate


def create_quiz_with_questions(quiz: QuizCreate, db: Session):
    db_quiz = LessonQuiz(title=quiz.title, lesson_id=quiz.lesson_id, max_attempts=quiz.max_attempts or 1)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    for q in quiz.questions:
        question = QuizQuestion(
            quiz_id=db_quiz.id,
            question=q.question,
            choices=q.choices,
            correct_answer=q.correct_answer
        )
        if question.correct_answer not in question.choices:
            raise HTTPException(status_code=400,
                                detail=f"Correct answer must be in choices for question: {question.question}")
        db.add(question)

    db.commit()
    return UJSONResponse(status_code=201, content={"message": "Quiz created", "quiz_id": db_quiz.id})


def get_quiz_by_lesson(lesson_id: int, user_id: int, db: Session):
    quiz = db.query(LessonQuiz).filter_by(lesson_id=lesson_id).first()
    if not quiz:
        return None

    questions = db.query(QuizQuestion).filter_by(quiz_id=quiz.id).all()

    # Get all results by this user for this quiz
    results = db.query(StudentQuizResult).filter_by(
        quiz_id=quiz.id,
        user_id=user_id
    ).order_by(StudentQuizResult.id.desc()).all()

    latest_result = results[0] if results else None

    return {
        "quiz_id": quiz.id,
        "title": quiz.title,
        "max_attempts": quiz.max_attempts,
        "submitted_attempts": len(results),
        "score": latest_result.score if latest_result else None,
        "selected_answers": latest_result.selected_answers if latest_result else {},
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "choices": q.choices,
            } for q in questions
        ]
    }


def find_quiz_by_id(quiz_id: int, db: Session):
    quiz = db.query(LessonQuiz).filter_by(id=quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


def submit_quiz(quiz: LessonQuiz, submission, user_id: int, db: Session):
    # Check attempt limit
    attempt_count = db.query(StudentQuizResult).filter_by(
        user_id=user_id, quiz_id=quiz.id
    ).count()
    if attempt_count >= quiz.max_attempts:
        raise HTTPException(status_code=400, detail="Maximum attempts reached for this quiz")

    # Load questions and calculate score
    questions = db.query(QuizQuestion).filter_by(quiz_id=quiz.id).all()
    correct_map = {q.id: q.correct_answer for q in questions}

    correct_count = sum(
        1 for ans in submission.answers
        if correct_map.get(ans.question_id) == ans.selected
    )
    percent_score = round((correct_count / len(questions)) * 100)

    # Update lesson progress
    lesson_id = quiz.lesson_id
    passed = percent_score >= quiz.passing_score

    progress = db.query(UserLessonProgress).filter_by(
        user_id=user_id, lesson_id=lesson_id
    ).first()

    if progress:
        progress.is_completed = passed
    else:
        db.add(UserLessonProgress(user_id=user_id, lesson_id=lesson_id, is_completed=passed))

    # Save quiz result
    result = StudentQuizResult(
        user_id=user_id,
        quiz_id=quiz.id,
        selected_answers={a.question_id: a.selected for a in submission.answers},
        score=percent_score,
        submitted_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()

    return UJSONResponse(status_code=200, content={
        "message": "Quiz submitted",
        "score": percent_score,
        "total": len(questions)
    })


def get_lesson_completion_status(user_id: int, lesson_id: int, db):
    quizzes = db.query(LessonQuiz).filter_by(lesson_id=lesson_id).all()
    if not quizzes:
        return False  # no quiz means cannot be completed

    quiz_ids = [q.id for q in quizzes]
    result = db.query(StudentQuizResult).filter(
        StudentQuizResult.quiz_id.in_(quiz_ids),
        StudentQuizResult.user_id == user_id
    ).order_by(StudentQuizResult.id.desc()).first()
    if not result:
        return False

    total_questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id.in_(quiz_ids)).count()
    return result.score >= 0.6 * total_questions  # 60% threshold


# todo update function to handle multiple quizzes and threshold.

def update_quiz(quiz_id: int, data: QuizUpdate, db: Session):
    quiz = db.query(LessonQuiz).filter_by(id=quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if data.title:
        quiz.title = data.title

    for updated in data.questions:
        question = db.query(QuizQuestion).filter_by(id=updated.id, quiz_id=quiz_id).first()
        if question:
            question.question = updated.question
            question.choices = updated.choices
            question.correct_answer = updated.correct_answer

    db.commit()
    return UJSONResponse(status_code=200, content={"message": "Quiz updated successfully"})


def delete_quiz(quiz_id: int, db: Session):
    quiz = db.query(LessonQuiz).filter_by(id=quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if db.query(StudentQuizResult).filter_by(quiz_id=quiz_id).count() > 0:
        raise HTTPException(status_code=400, detail="Cannot delete a quiz that has submissions.")

    db.query(QuizQuestion).filter_by(quiz_id=quiz_id).delete()
    db.delete(quiz)
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)


def get_quiz_results(quiz_id: int, db: Session):
    results = (
        db.query(StudentQuizResult, User)
        .join(User, StudentQuizResult.user_id == User.id)
        .filter(StudentQuizResult.quiz_id == quiz_id)
        .order_by(StudentQuizResult.submitted_at.desc())
        .all()
    )

    return UJSONResponse(status_code=200, content=[
        {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "score": result.score,
            "submitted_at": result.submitted_at,
            "selected_answers": result.selected_answers,
        }
        for result, user in results
    ])
