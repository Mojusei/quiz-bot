# database/crud.py
from sqlalchemy.ext.asyncio import AsyncSession

from models.quiz import QuizState


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
