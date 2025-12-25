# bot/handlers/stats.py
from aiogram import Router, types
from aiogram.filters import Command

from database.engine import AsyncSessionLocal
from database.crud import get_last_result, get_top_players


router = Router()


@router.message(Command("stats"))
async def show_stats(message: types.Message):
    async with AsyncSessionLocal() as session:
        last = await get_last_result(session, message.from_user.id)
        top_players = await get_top_players(session, limit=5)

    if last:
        text = (
            f"📊 Ваш последний результат:\n"
            f"✅ Правильных: {last.correct_answers} "
            f"из {last.total_questions}\n\n"
        )
    else:
        text = "Вы ещё не проходили квиз.\n\n"

    text += "🏆 Топ-5 игроков:\n"
    if top_players:
        for i, player in enumerate(top_players, 1):
            text += f"{i}. 👤 ID {player.user_id}: "
            f"{player.correct_answers}/{player.total_questions}\n"
    else:
        text += "Никто пока не прошёл квиз."

    await message.answer(text)
