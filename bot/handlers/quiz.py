# bot/handlers/quiz.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from database.crud import get_quiz_index, update_quiz_index
from database.engine import AsyncSessionLocal
from bot.keyboards import generate_options_keyboard
from quiz_data import quiz_data
from models.quiz import QuizResult, QuizState

router = Router()


@router.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    chosen_index = int(callback.data.split("_", maxsplit=1)[1])

    async with AsyncSessionLocal() as session:
        state = await session.get(QuizState, callback.from_user.id)
        if state is None:
            state = QuizState(
                user_id=callback.from_user.id,
                question_index=0,
                correct_answers=0
            )
            session.add(state)
            await session.commit()
            await session.refresh(state)

        current_index = state.question_index

        # Защита от несогласованности (на всякий случай)
        if current_index >= len(quiz_data):
            await callback.message.answer("Квиз уже завершён.")
            return

        # Получаем данные вопроса
        question = quiz_data[current_index]
        correct_index = question["correct_option"]
        chosen_text = question["options"][chosen_index]
        correct_text = question["options"][correct_index]
        is_correct = (chosen_index == correct_index)

        # Обновляем счётчик правильных ответов
        if is_correct:
            state.correct_answers += 1

        # Переходим к следующему вопросу (или завершаем)
        state.question_index = current_index + 1
        await session.commit()

    # Отправляем пользователю его выбор и результат
    if is_correct:
        result_text = "✅ Верно!"
    else:
        result_text = f"❌ Неверно.\nПравильный ответ: {correct_text}"

    await callback.message.answer(
        f"Ваш ответ: {chosen_text}\n\n{result_text}"
    )

    # Проверяем завершение квиза
    if current_index + 1 >= len(quiz_data):
        async with AsyncSessionLocal() as session:
            # Получаем актуальное состояние (с финальным счётом)
            final_state = await session.get(QuizState, callback.from_user.id)
            if final_state:
                # Сохраняем результат прохождения
                result = QuizResult(
                    user_id=callback.from_user.id,
                    correct_answers=final_state.correct_answers,
                    total_questions=len(quiz_data)
                )
                session.add(result)
                await session.commit()

        await callback.message.answer("🎉 Квиз завершён! Спасибо за участие.")
    else:
        # Переходим к следующему вопросу
        await send_question(callback.message, callback.from_user.id)


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
