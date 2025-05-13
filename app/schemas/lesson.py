from pydantic import BaseModel

from app.schemas.quiz import QuizDetailResponse


class LessonBase(BaseModel):
    title: str
    content: str = ""


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonResponse(LessonBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True


class SimpleLessonResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class LessonDetailResponse(LessonBase):
    id: int
    quiz: list[QuizDetailResponse] = []
    class Config:
        from_attributes = True