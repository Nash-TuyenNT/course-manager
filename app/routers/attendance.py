from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import attendance as attendance_crud
from app.crud import course as course_crud
from app.database import SessionLocal
from app.enums.actions import Actions
from app.enums.resourses import Resources
from app.models.user import User
from app.roles.permission import check_permission
from app.schemas.attendance import (
    AttendanceSessionCreate, AttendanceSessionResponse,
    StudentAttendanceResponse
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/attendances", tags=["Attendance"])


@router.post("/sessions", response_model=AttendanceSessionResponse)
def create_session(
        data: AttendanceSessionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    check_permission(current_user, Actions.CREATE, Resources.ATTENDANCE)

    return attendance_crud.create_attendance_session(data, current_user.id, db)


@router.post("/check-in/{session_id}", response_model=StudentAttendanceResponse)
def check_in(
        session_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    attendance_session = attendance_crud.find_attendance_session(session_id, db)
    check_permission(current_user, Actions.UPDATE, Resources.ATTENDANCE, attendance_session)

    return attendance_crud.mark_attendance(current_user.id, session_id, db)


@router.get("/course/{course_id}", response_model=List[StudentAttendanceResponse])
def list_attendance(
        course_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    course = course_crud.find_course(course_id, db)
    check_permission(current_user, Actions.MANAGE, Resources.COURSE, course)
    check_permission(current_user, Actions.MANAGE, Resources.ATTENDANCE)

    return attendance_crud.get_attendance_by_course(course_id, db)
