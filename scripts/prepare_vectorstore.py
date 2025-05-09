from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy.orm import joinedload

from app.config import settings
from app.database import SessionLocal
from app.models.course import Course
from app.models.user_course import UserCourse
from app.models.lesson import Lesson
from app.models.user import User
from app.models.quiz_models import LessonQuiz

CHROMA_DIR = "../db/"

embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.google_embeddings_model,
    google_api_key=settings.google_api_key
)


def fetch_documents_from_db():
    db = SessionLocal()
    documents = []

    courses = db.query(Course).options(
        joinedload(Course.lessons),
        joinedload(Course.creator),
        joinedload(Course.users).joinedload(UserCourse.user)  # load enrolled users
    ).all()

    for course in courses:
        # Lấy thông tin cơ bản
        course_title = course.title
        course_description = course.description or ""
        creator_name = course.creator.username if course.creator else "Không rõ"
        total_users = len(course.users)

        # Ghép nội dung lesson
        lesson_summary = ""
        for lesson in course.lessons:
            lesson_summary += f"\n---\n[Lesson] {lesson.title}\n{lesson.content or ''}"

        # Tổng hợp lại 1 document cho mỗi course
        full_text = (
            f"[Course] {course_title}\n"
            f"Mô tả: {course_description}\n"
            f"Người tạo: {creator_name}\n"
            f"Số học viên đã tham gia: {total_users}\n"
            f"{lesson_summary}"
        )

        documents.append(Document(
            page_content=full_text,
            metadata={
                "course_id": course.id,
                "title": course_title,
                "type": "course"
            }
        ))

    db.close()
    return documents


def build_vectorstore():
    documents = fetch_documents_from_db()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectordb.persist()
    print(f"✅ Vectorstore saved to 'db/' with {len(documents)} documents.")


if __name__ == "__main__":
    build_vectorstore()
