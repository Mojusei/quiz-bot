# bot/keyboards.py
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quiz_data import quiz_data


def generate_options_keyboard(question_index: int):
    opts = quiz_data[question_index]["options"]
    correct = opts[quiz_data[question_index]["correct_option"]]
    builder = InlineKeyboardBuilder()
    for opt in opts:
        builder.add(
            InlineKeyboardButton(
                text=opt,
                callback_data=(
                    "right_answer" if opt == correct else "wrong_answer"
                )
            )
        )
    builder.adjust(1)
    return builder.as_markup()
