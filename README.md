```markdown
# Course Manager Backend (FastAPI)

This project is the backend system for a full-featured Course Manager application, built using FastAPI and PostgreSQL.

It supports student enrollment, lesson and quiz management, attendance tracking, progress monitoring, and role-based access control for students, teachers, and administrators.

# Requirements
- Python 3.10 or higher  
  *(Recommended: Python 3.10.x or 3.11.x for FastAPI and Pydantic v2 compatibility)*  
- PostgreSQL 13 or higher  

# INSTALLATION GUIDE
1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/course-manager-backend.git
   cd course-manager-backend
   ```

2. Create and Activate a Virtual Environment:

   **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Mac/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:  
   Create a `.env` file for database URL, API keys, etc.

   Example `.env` file:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/course_manager_db
   GOOGLE_API_KEY=your_google_api_key
   ```

5. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

# Features

🧑‍🏫 **Courses and Lessons**
1. Teachers/Admins can create, update, delete courses.
2. Each course contains multiple lessons.
3. Ownership control: teachers can only edit their own courses.

👨‍🎓 **Student Enrollment**
1. Students can enroll in available courses.
2. Teachers can manually enroll students.
3. Enrollment restricted to users with a student role.

📝 **Quizzes System**
1. Teachers can create quizzes linked to lessons.
2. Each quiz can have multiple questions.
3. Configurable maximum attempts and passing scores.
4. Students submit quizzes, and lesson progress is updated automatically based on quiz results.

📈 **Progress Tracking**
1. Track lesson completion automatically.
2. Calculate course completion percentage for students.
3. Mark courses completed only when all lessons are passed.

📅 **Attendance System**
1. Teachers/Admins can create attendance sessions (manual, auto, quiz-based).
2. Students can check-in during the allowed time window.
3. Attendance records are linked to courses and lessons.

🔐 **Authentication & Authorization**
- JWT-based login system (access token and refresh token strategy).
- Attribute-Based Access Control (ABAC) (Student, Teacher, Admin).
- Session timeout handling with token refresh.

🤖 **AI-Powered Chatbot**
- Integrated with Google Generative AI (Gemini 2.0) for answering course-related questions.
- Supports web search using SerpAPI for additional information.
- Maintains conversation history for context-aware responses.

👑 **Admin Panel**
1. Manage users (list, search, view roles).
2. Manage courses (view all, edit, delete).
3. View enrollment and completion statistics.
4. *(Planned)* Export system data (users, courses, quiz results) to CSV.
5. *(Planned)* Track login activities for security.

# Technology Stack

| Layer            | Technology                  |
|-------------------|-----------------------------|
| **Backend**       | FastAPI (Python)           |
| **Database**      | PostgreSQL                 |
| **ORM**           | SQLAlchemy                 |
| **Authentication**| OAuth2 + JWT (PyJWT)       |
| **Migrations**    | Alembic                    |
| **Frontend**      | ReactJS (separate repo)    |
| **HTTP Requests** | Axios                      |
| **AI Integration**| Google Generative AI (Gemini 2.0), SerpAPI |

# Development Notes
- Ensure the `.env` file is properly configured with valid API keys and database credentials.
- Use `pytest` for running unit tests.
- Follow PEP 8 coding standards for consistency.
```