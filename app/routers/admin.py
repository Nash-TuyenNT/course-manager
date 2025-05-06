from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import admin as admin_crud
from app.database import SessionLocal
from app.enums.roles import Roles
from app.models.user import User
from app.schemas.course import CourseAdminResponse, CourseDetailResponse, CourseUpdate
from app.schemas.user import UserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_admin(user: User = Depends(get_current_user)):
    if user.role != Roles.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@router.get("/overview")
def get_admin_overview(
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_admin_dashboard_data(db)


@router.get("/users", response_model=list[UserResponse])
def list_users(
        search: Optional[str] = Query(None),
        role: Optional[Roles] = Query(None),
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_all_users(db, search=search, role=role)


@router.get("/courses", response_model=List[CourseAdminResponse])
def get_all_courses(
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_all_courses_with_stats(db)


@router.get("/courses/{course_id}/details", response_model=CourseDetailResponse)
def view_course_details(
        course_id: int,
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.get_course_details(course_id, db)


@router.put("/courses/{course_id}", response_model=CourseAdminResponse)
def update_course(
        course_id: int,
        update_data: CourseUpdate,
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.update_course(course_id, update_data, db)


@router.delete("/courses/{course_id}")
def delete_course(
        course_id: int,
        db: Session = Depends(get_db),
        current_admin: User = Depends(verify_admin)
):
    return admin_crud.delete_course(course_id, db)
