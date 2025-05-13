from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import lesson as lesson_crud
from app.crud import course as course_crud
from app.crud import quiz as quiz_crud
from app.database import SessionLocal
from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.models.user import User
from app.roles.permission import check_permission
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse, LessonDetailResponse

router = APIRouter(prefix="/lessons", tags=["lessons"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/course/{course_id}", response_model=LessonResponse)
def create_lesson(course_id: int, lesson: LessonCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.MANAGE, Resources.COURSE, course)
    check_permission(current_user, Actions.CREATE, Resources.LESSON)

    return lesson_crud.create_lesson(course_id, lesson, db, current_user.id)


@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_lessons(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_permission(current_user, Actions.READ, Resources.COURSE)
    check_permission(current_user, Actions.READ, Resources.LESSON)

    return lesson_crud.get_lessons(course_id, db)


@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, update: LessonUpdate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    lesson = lesson_crud.find_lesson(lesson_id, db)
    check_permission(current_user, Actions.UPDATE, Resources.COURSE, lesson.course)
    check_permission(current_user, Actions.UPDATE, Resources.LESSON, lesson)

    return lesson_crud.update_lesson(lesson, update, db)


@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = lesson_crud.find_lesson(lesson_id, db)
    check_permission(current_user, Actions.DELETE, Resources.LESSON, lesson)

    return lesson_crud.delete_lesson(lesson, db)


@router.get("/course/{course_id}/with-progress")
def get_lessons_with_progress(course_id: int, db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.VIEW_STATUS, Resources.COURSE, course)

    return lesson_crud.get_lessons_with_progress(course_id, db, current_user)


@router.get("/{lesson_id}/completed")
def is_lesson_completed(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = lesson_crud.find_lesson(lesson_id, db)
    check_permission(current_user, Actions.VIEW_STATUS, Resources.LESSON, lesson)

    completed = quiz_crud.get_lesson_completion_status(current_user.id, lesson_id, db)
    return UJSONResponse(status_code=HTTPStatus.OK, content={"lesson_id": lesson_id, "is_completed": completed})

@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = lesson_crud.find_lesson(lesson_id, db)
    check_permission(current_user, Actions.READ, Resources.LESSON, lesson)

    return LessonDetailResponse.model_validate(lesson, from_attributes=True)