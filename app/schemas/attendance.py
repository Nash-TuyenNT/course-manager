from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttendanceSessionCreate(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    type: str  # manual / auto / quiz-based

class AttendanceSessionResponse(AttendanceSessionCreate):
    id: int
    class Config:
        from_attributes = True

class StudentAttendanceResponse(BaseModel):
    id: int
    user_id: int
    attendance_session_id: int
    status: str
    timestamp: datetime
    class Config:
        from_attributes = True
