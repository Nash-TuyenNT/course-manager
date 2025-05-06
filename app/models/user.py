from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.enums.roles import Roles
from app.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Roles), nullable=False)

    created_courses = relationship("Course", back_populates="creator")
    # store the courses which user is enrolling
    courses = relationship("UserCourse", back_populates="user")
