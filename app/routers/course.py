from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..crud import course as course_crud
from ..database import SessionLocal
from ..enums.actions import Actions
from ..enums.resourses import Resources
from ..models.user import User
from ..roles.permission import check_permission
from ..schemas import course as course_schema
from ..schemas import user as user_schema
from ..schemas.course import CourseWithLesson

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new course
@router.post("/", response_model=course_schema.CourseResponse)
def create_course(course: course_schema.CourseCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    check_permission(current_user, Actions.CREATE, Resources.COURSE)

    return course_crud.create_course(db=db, course=course, creator_id=current_user.id)


@router.get("/{course_id}", response_model=course_schema.CourseWithLesson)
def get_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.READ, Resources.COURSE, course)

    is_enrolled = False
    is_completed = False
    enrolled = next((uc for uc in course.users if uc.user_id == current_user.id), None)
    if enrolled:
        is_enrolled = True
        if enrolled.is_completed:
            is_completed = True

    return CourseWithLesson.model_validate(course, from_attributes=True).model_copy(update={
        "is_enrolled": is_enrolled,
        "is_completed": is_completed
    })


# Update an existing course
@router.put("/{course_id}", response_model=course_schema.CourseResponse)
def update_course(course_id: int, new_course: course_schema.CourseUpdate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.UPDATE, Resources.COURSE, course)

    return course_crud.update_course(db, course, new_course)


# Teacher enroll a user to specific course
@router.post("/{course_id}/enroll-user/{user_id}")
def enroll_user_by_teacher(course_id: int, user_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.MANAGE, Resources.COURSE, course)

    return course_crud.enroll_user_by_teacher(course_id, user_id, db)


# Mark course as completed
@router.patch("/{course_id}/complete")
def mark_course_complete(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.COMPLETE, Resources.COURSE, course)

    return course_crud.mark_course_complete(course_id, current_user.id, db)


# Get all courses
@router.get("/", response_model=List[course_schema.CourseResponse])
def get_courses(creator: int | None = None, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    check_permission(current_user, Actions.READ, Resources.COURSE)

    return course_crud.get_courses(creator, db=db)


# Enroll user in course by themselves
@router.post("/{course_id}/enroll")
def enroll_user(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.ENROLL, Resources.COURSE, course)

    return course_crud.enroll_user(user_id=current_user.id, course_id=course_id, db=db)


# get all enrolled courses of a student
@router.get("/by-user/{user_id}", response_model=List[course_schema.CourseWithProgress])
def get_courses_by_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return course_crud.get_courses_by_user(user_id, db)


# get enrolled students in a Course
@router.get("/by-course/{course_id}/users", response_model=List[user_schema.UserResponse])
def get_users_by_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.MANAGE, Resources.COURSE, course)

    return course_crud.get_users_by_course(course_id, db, current_user.id)


# delete course by id
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.DELETE, Resources.COURSE, course)

    return course_crud.delete_course(course, db)
