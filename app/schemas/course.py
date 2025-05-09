from pydantic import BaseModel

from app.schemas.lesson import SimpleLessonResponse
from app.schemas.user import SimpleUserResponse


class CourseBase(BaseModel):
    title: str
    description: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    creator_id: int

class CourseResponse(CourseBase):
    id: int
    creator_id: int
    class Config:
        orm_mode = True

class CourseWithProgress(CourseBase):
    id: int
    creator_id: int
    progress: int = 0
    is_completed: bool

class CourseWithLesson(CourseResponse):
    lessons: list[SimpleLessonResponse] = []
    is_enrolled: bool = False
    is_completed: bool = False

class CreatorInCourse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class CourseAdminResponse(BaseModel):
    id: int
    title: str
    description: str
    creator: CreatorInCourse
    total_students: int
    lesson_count: int
    avg_completion_rate: float

    class Config:
        orm_mode = True

class CourseDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    creator: SimpleUserResponse
    lessons: list[SimpleLessonResponse]
    users: list[SimpleUserResponse]

    class Config:
        orm_mode = True
