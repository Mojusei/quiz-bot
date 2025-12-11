# bot/handlers/start.py
from aiogram import Router, types
from aiogram.types import Message, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
