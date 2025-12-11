# bot/handlers/quiz.py
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from database.crud import get_quiz_index, update_quiz_index
from bot.keyboards import generate_options_keyboard
from quiz_data import quiz_data


router = Router()


@router.callback_query(F.data == "right_answer")
async def right_answer(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Верно!")

    async with AsyncSessionLocal() as session:
        current = await get_quiz_index(session, callback.from_user.id)
        await update_quiz_index(session, callback.from_user.id, current + 1)

    if current + 1 < len(quiz_data):
        await send_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Квиз завершён!")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    async with AsyncSessionLocal() as session:
        current = await get_quiz_index(session, callback.from_user.id)

    correct_text = (
        quiz_data[current]["options"][quiz_data[current]["correct_option"]]
    )
    await callback.message.answer(
        f"Неправильно. Правильный ответ: {correct_text}"
        )

    async with AsyncSessionLocal() as session:
        await update_quiz_index(session, callback.from_user.id, current + 1)

    if current + 1 < len(quiz_data):
        await send_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Квиз завершён!")


async def send_question(message: Message, user_id: int):
    async with AsyncSessionLocal() as session:
        index = await get_quiz_index(session, user_id)
    markup = generate_options_keyboard(index)
    await message.answer(quiz_data[index]["question"], reply_markup=markup)


@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: Message):
    await message.answer("Давайте начнем квиз!")
    async with AsyncSessionLocal() as session:
        await update_quiz_index(session, message.from_user.id, 0)
    await send_question(message, message.from_user.id)
