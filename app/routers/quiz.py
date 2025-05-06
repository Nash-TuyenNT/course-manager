import csv
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import quiz as quiz_crud
from app.crud import lesson as lesson_crud
from app.database import SessionLocal
from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.models.user import User
from app.roles.permission import check_permission
from app.schemas.quiz import QuizCreate, QuizSubmitRequest, QuizUpdate

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_permission(current_user, Actions.CREATE, Resources.QUIZ)

    return quiz_crud.create_quiz_with_questions(quiz, db)


@router.get("/by-lesson/{lesson_id}")
def get_quiz_by_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = lesson_crud.find_lesson(lesson_id, db)
    check_permission(current_user, Actions.VIEW_STATUS, Resources.LESSON, lesson)
    quiz = quiz_crud.get_quiz_by_lesson(lesson_id, current_user.id, db)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.post("/submit")
def submit_quiz(submission: QuizSubmitRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    quiz = quiz_crud.find_quiz_by_id(submission.quiz_id, db)
    check_permission(current_user, Actions.SUBMIT, Resources.QUIZ, quiz)

    return quiz_crud.submit_quiz(quiz, submission, user_id=current_user.id, db=db)


@router.put("/{quiz_id}")
def update_quiz(quiz_id: int, data: QuizUpdate, db: Session = Depends(get_db)):
    return quiz_crud.update_quiz(quiz_id, data, db)


@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return quiz_crud.delete_quiz(quiz_id, db)


@router.get("/{quiz_id}/results")
def get_quiz_results(
        quiz_id: int,
        db: Session = Depends(get_db)
):
    # Optional: Check if user is a teacher/owner of the course
    return quiz_crud.get_quiz_results(quiz_id, db)


@router.get("/{quiz_id}/results/export")
def export_quiz_results_csv(
        quiz_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    results = quiz_crud.get_quiz_results(quiz_id, db)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Username", "Email", "Score", "Submitted At", "Answers"])

    for r in results:
        answer_str = "; ".join([f"Q{qid}: {ans}" for qid, ans in r["selected_answers"].items()])
        writer.writerow([r["username"], r["email"], r["score"], r["submitted_at"], answer_str])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": f"attachment; filename=quiz_{quiz_id}_results.csv"
    })
