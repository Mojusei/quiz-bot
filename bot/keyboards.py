# bot/keyboards.py
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quiz_data import quiz_data


def generate_options_keyboard(question_index: int):
    opts = quiz_data[question_index]["options"]
    builder = InlineKeyboardBuilder()
    for i, opt in enumerate(opts):
        builder.add(InlineKeyboardButton(
            text=opt, callback_data=f"answer_{i}"
            ))
    builder.adjust(1)
    return builder.as_markup()
