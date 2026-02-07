import logging
import asyncio

from aiogram.fsm.context import FSMContext
from src.Sender.broadcast import BroadcastState
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.Sender.broadcast import BroadcastState
from src.user_manager import is_admin,is_superadmin
from src.db import Database
from src.config import ADMIN, SUPERADMIN, TOKEN

rt = Router()
db = Database()
bot = Bot(token=TOKEN)


MAX_MESSAGE_LENGTH = 4096  # лимит Telegram

async def send_long_message(bot: Bot, chat_id: int, text: str):
    """
    Разбивает длинное сообщение на части и отправляет их последовательно.
    """
    if len(text) <= MAX_MESSAGE_LENGTH:
        await bot.send_message(chat_id, text)
    else:
        for i in range(0, len(text), MAX_MESSAGE_LENGTH):
            await bot.send_message(chat_id, text[i:i+MAX_MESSAGE_LENGTH])


@rt.message(Command("question"))
@rt.message(F.text == "Вопросы")
@rt.message(F.text == "Смотреть вопросы")
async def question_list(message: Message, state: FSMContext) -> None:
    if is_admin(message.from_user.id):
        question_list = []
        connection = db.create_connection()
        cursor = connection.cursor()

        # Выбираем все вопросы
        cursor.execute('SELECT * FROM questions')
        questions = cursor.fetchall()

        connection.close()

        # Формируем список вопросов с датами
        for question in questions:
            question_list.append(f"{question[0]}. {question[2]}")

        if question_list:
            full_text = "\n".join(question_list)
            # используем новую функцию для длинных сообщений
            await send_long_message(bot, message.chat.id, full_text)
        else:
            await message.answer("Вопросы отсутствуют")
    else:
        await state.set_state(BroadcastState.question)
        await message.answer("Напиши свой вопрос, он будет отправлен анонимно")

@rt.message(Command("cleardb"))
async def clear_db_handler(message: Message, state: FSMContext):
    if not is_superadmin(message.from_user.id):
        print("Someone tryed clear db User ID:", message.from_user.id)
        await message.answer("⛔ У тебя нет прав")
        return
    elif is_superadmin(message.from_user.id):
        await message.answer("🧹 Очищаю базу данных...")
        await asyncio.to_thread(db.clear_db)
        await message.answer("✅ База данных успешно очищена")
