from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import Session
from starlette.responses import Response

from ..enums.roles import Roles
from ..models.course import Course
from ..models.lesson import Lesson
from ..models.user import User
from ..models.user_course import UserCourse
from ..models.user_lesson_progress import UserLessonProgress
from ..schemas import course as schema
from ..schemas.course import CourseWithProgress


def create_course(db: Session, course: schema.CourseCreate, creator_id: int):
    db_course = Course(**course.dict(), creator_id=creator_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, db_course: Course, course: schema.CourseUpdate):
    db_course.title = course.title
    db_course.description = course.description
    db.commit()
    db.refresh(db_course)
    return db_course


def mark_course_complete(course_id: int, current_user_id: int, db: Session):
    # Get all lessons in the course
    lessons = db.query(Lesson).filter_by(course_id=course_id).all()
    if not lessons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No lessons found in course")

    # Get completed lessons by student
    completed_ids = set(
        row.lesson_id for row in db.query(UserLessonProgress)
        .filter_by(user_id=current_user_id, is_completed=True)
        .filter(UserLessonProgress.lesson_id.in_([l.id for l in lessons]))
        .all()
    )

    if len(completed_ids) != len(lessons):
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail="Please complete all lessons before finishing the course")

    # Update status
    enrollment = db.query(UserCourse).filter_by(user_id=current_user_id, course_id=course_id).first()
    enrollment.is_completed = True
    db.commit()
    return UJSONResponse(status_code=HTTPStatus.OK, content={"message": "Course marked as completed"})


def get_courses(db: Session):
    return db.query(Course).all()


def enroll_user(user_id: int, course_id: int, db: Session):
    # Check if already enrolled
    existing = db.query(UserCourse).filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return UJSONResponse(status_code=HTTPStatus.OK, content={"message": "Already enrolled"})

    enrollment = UserCourse(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return UJSONResponse(status_code=HTTPStatus.OK, content={"message": "Enrolled successfully"})


def get_courses_by_user(user_id: int, db: Session):
    # Corrected query: get actual users
    courses = db.query(Course).join(UserCourse).filter(UserCourse.user_id == user_id).all()
    response = []

    for course in courses:
        lessons = db.query(Lesson).filter_by(course_id=course.id).all()
        total = len(lessons)

        completed = db.query(UserLessonProgress).filter_by(user_id=user_id, is_completed=True) \
            .filter(UserLessonProgress.lesson_id.in_([l.id for l in lessons])).count()

        progress = int((completed / total) * 100) if total > 0 else 0

        response.append(CourseWithProgress(
            id=course.id,
            title=course.title,
            description=course.description,
            creator_id=course.creator_id,
            is_completed=any(uc.is_completed for uc in course.users if uc.user_id == user_id),
            progress=progress
        ))

    return response


def get_users_by_course(course_id: int, db: Session, current_user_id: int):
    course = db.query(Course).get(course_id)
    if not course:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Course not found")
    if course.creator_id != current_user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not allowed to view students in this course")

    # Corrected query: get actual users
    users = db.query(User).join(UserCourse).filter(UserCourse.course_id == course.id).all()
    return users


def enroll_user_by_teacher(course_id: int, user_id: int, db: Session):
    student = db.query(User).filter(User.id == user_id).first()

    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")
    if student.role != Roles.student:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail="This user is not a student-role User. Please enroll student only!")

    # Check if already enrolled
    existing = db.query(UserCourse).filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return UJSONResponse(status_code=HTTPStatus.OK, content={"message": "User already enrolled"})

    enrollment = UserCourse(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    return UJSONResponse(status_code=HTTPStatus.OK, content={"message": "User enrolled successfully"})


def find_course(course_id: int, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Course not found")
    return course


def delete_course(course: Course, db: Session):
    db.delete(course)
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
