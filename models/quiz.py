# models/quiz.py
from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class QuizState(Base):
    __tablename__ = "quiz_state"

    user_id = Column(Integer, primary_key=True, index=True)
    question_index = Column(Integer, default=0)
