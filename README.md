# Course Manager Backend (FastAPI)

This project is the backend system for a full-featured Course Manager application, built using FastAPI and PostgreSQL.

It supports student enrollment, lesson and quiz management, attendance tracking, progress monitoring, and role-based access control for students, teachers, and administrators.

# Requirements
Python 3.10 or higher
(Recommended: Python 3.10.x or 3.11.x for FastAPI and Pydantic v2 compatibility)

PostgreSQL 13 or higher

# INSTALLATION GUIDE
1. Clone the repository:

git clone https://github.com/your-username/course-manager-backend.git

cd course-manager-backend

2. Create and Activate a Virtual Environment:

Windows

      python -m venv venv

      venv\Scripts\activate

Mac/Linux

      python3 -m venv venv

      source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt

3. Configure environment variables:
Create a .env file for database URL, etc.

DATABASE_URL=postgresql://user:password@localhost:5432/course_manager_db

4. Start the FastAPI server:
uvicorn app.main:app --reload


# Features

🧑‍🏫 Courses and Lessons

1. Teachers/Admins can create, update, delete courses

2. Each course contains multiple lessons

3. Ownership control: teachers can only edit their own courses

👨‍🎓 Student Enrollment
1. Students can enroll in available courses

2. Teachers can manually enroll students

3. Enrollment restricted to users with a student role

📝 Quizzes System
1. Teachers can create quizzes linked to lessons

2. Each quiz can have multiple questions

3. Configurable maximum attempts and passing scores

4. Students submit quizzes, and lesson progress is updated automatically based on quiz results

📈 Progress Tracking
1. Track lesson completion automatically

2. Calculate course completion percentage for students

3. Mark courses completed only when all lessons are passed

📅 Attendance System
1. Teachers/Admins can create attendance sessions (manual, auto, quiz-based)

2. Students can check-in during the allowed time window

3. Attendance records are linked to courses and lessons

🔐 Authentication & Authorization

JWT-based login system (access token and refresh token strategy)

Attribute-Based Access Control (ABAC) (Student, Teacher, Admin)

Session timeout handling with token refresh

👑 Admin Panel

Manage users (list, search, view roles)

Manage courses (view all, edit, delete)

View enrollment and completion statistics

(Planned) Export system data (users, courses, quiz results) to CSV

(Planned) Track login activities for security

# Technology Stack

Layer	Technology

Backend	FastAPI (Python)

Database	PostgreSQL

ORM	SQLAlchemy

Authentication	OAuth2 + JWT (PyJWT)

Migrations	Alembic

Frontend	ReactJS (separate repo)

HTTP Requests	Axios