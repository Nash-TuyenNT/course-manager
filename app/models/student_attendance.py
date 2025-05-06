from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from app.models import Base


class AttendanceSession(Base):
    __tablename__ = 'attendance_sessions'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    type = Column(String)  # manual / auto / quiz-based

    course = relationship('Course')
    lesson = relationship('Lesson')


class StudentAttendance(Base):
    __tablename__ = 'student_attendance'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    attendance_session_id = Column(Integer, ForeignKey('attendance_sessions.id'))
    status = Column(String)  # present / absent
    timestamp = Column(DateTime)

    user = relationship('User')
    session = relationship('AttendanceSession')
