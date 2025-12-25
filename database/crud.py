# database/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from models.quiz import QuizState, QuizResult


async def get_quiz_index(session: AsyncSession, user_id: int) -> int:
    result = await session.get(QuizState, user_id)
    return result.question_index if result else 0


async def update_quiz_index(session: AsyncSession, user_id: int, index: int):
    state = await session.get(QuizState, user_id)
    if state:
        state.question_index = index
    else:
        state = QuizState(user_id=user_id, question_index=index)
        session.add(state)
    await session.commit()


async def save_quiz_result(
        session: AsyncSession, user_id: int, correct: int, total: int
        ):
    result = QuizResult(
        user_id=user_id, correct_answers=correct, total_questions=total
        )
    session.add(result)
    await session.commit()


async def get_last_result(session: AsyncSession, user_id: int):
    stmt = (
        select(QuizResult)
        .where(QuizResult.user_id == user_id)
        .order_by(desc(QuizResult.completed_at))
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_top_players(session: AsyncSession, limit: int = 5):
    subq = (
        select(
            QuizResult.user_id,
            QuizResult.correct_answers,
            QuizResult.total_questions,
            QuizResult.completed_at
        )
        .distinct(QuizResult.user_id)
        .order_by(QuizResult.user_id, desc(QuizResult.completed_at))
        .subquery()
    )
    stmt = (
        select(subq)
        .order_by(desc(subq.c.correct_answers))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.fetchall()
