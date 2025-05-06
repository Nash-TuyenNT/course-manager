from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)  # Optional lesson body
    course_id = Column(Integer, ForeignKey("courses.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))

    course = relationship("Course", back_populates="lessons")
    quiz = relationship("LessonQuiz", back_populates="lesson")
