from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.models.user_lesson_progress import UserLessonProgress
from app.schemas.lesson import LessonCreate, LessonUpdate


def create_lesson(course_id: int, lesson: LessonCreate, db: Session, current_user_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Course not found")
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You are not the owner of this course")

    new_lesson = Lesson(title=lesson.title, content=lesson.content, course_id=course_id, creator_id=current_user_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


def get_lessons(course_id: int, db: Session):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    return lessons


def find_lesson(lesson_id: int, db: Session):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


def update_lesson(lesson: Lesson, update: LessonUpdate, db: Session):
    lesson.title = update.title
    lesson.content = update.content
    db.commit()
    db.refresh(lesson)
    return lesson


def delete_lesson(lesson: Lesson, db: Session):
    db.delete(lesson)
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)


def get_lessons_with_progress(course_id: int, db: Session, current_user: User):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    progress_map = {
        row.lesson_id: row.is_completed
        for row in db.query(UserLessonProgress).filter_by(user_id=current_user.id).all()
    }

    return [
        {
            "id": lesson.id,
            "title": lesson.title,
            "content": lesson.content,
            "is_completed": progress_map.get(lesson.id, False)
        }
        for lesson in lessons
    ]
