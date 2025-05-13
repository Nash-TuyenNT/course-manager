from typing import List, Optional

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    question: str
    choices: List[str]
    correct_answer: str

class QuizCreate(BaseModel):
    title: str
    lesson_id: int
    max_attempts: Optional[int] = 1
    questions: List[QuestionCreate]

class QuestionsResponse(BaseModel):
    id: int
    question: str
    choices: List[str]
    correct_answer: str

class QuizDetailResponse(BaseModel):
    id: int
    title: str
    max_attempts: int
    questions: List[QuestionsResponse] = []

class AnswerSubmit(BaseModel):
    question_id: int
    selected: str

class QuizSubmitRequest(BaseModel):
    quiz_id: int
    answers: List[AnswerSubmit]

class QuestionUpdate(BaseModel):
    id: int
    question: str
    choices: List[str]
    correct_answer: str

class QuizUpdate(BaseModel):
    title: Optional[str]
    questions: List[QuestionUpdate]
