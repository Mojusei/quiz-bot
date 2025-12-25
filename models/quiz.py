# models/quiz.py
from sqlalchemy import Integer, Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# models/quiz.py
class QuizState(Base):
    __tablename__ = "quiz_state"
    user_id = Column(Integer, primary_key=True, index=True)
    question_index = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)  # ← добавили сюда


class QuizResult(Base):
    __tablename__ = "quiz_result"
    user_id = Column(Integer, primary_key=True, index=True)
    correct_answers = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
