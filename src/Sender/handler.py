import logging
import sqlite3

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


@rt.message(Command("cleardb"))
async def clearr_db(message: Message) -> None:
    if is_superadmin(message.from_user.id) == True:
        Database.clear_db(db)
        await message.answer("Вы очистили базу данных...")


@rt.message(Command("question"))
@rt.message(F.text == "Вопросы")
@rt.message(F.text == "Смотреть вопросы")
async def question_list(message: Message, state: FSMContext) -> None:
    if is_admin(message.from_user.id) == True:
        question_list = []
        connection = sqlite3.connect(r'C:\Users\Pavel\OneDrive\Рабочий стол\Algoritms\Algoritms 1.0\Q&A\.venv\Lib\questions.db')
        cursor = connection.cursor()

        # Выбираем все вопросы
        cursor.execute('SELECT * FROM questions')
        questions = cursor.fetchall()

        # Закрытие соединения с базой данных
        connection.close()

        # Формируем список вопросов с датами
        for question in questions:
            # Предположим, что:
            # question[0] - это id
            # question[1] - это date (дата)
            # question[2] - это текст вопроса
            question_list.append(f"{question[0]}. {question[2]}")

        # Если вопросы есть, отправляем их
        if question_list:
            await message.answer("\n".join(question_list))  # Преобразуем список в строку с переносами
        else:
            await message.answer("Вопросы отсутствуют")
    else:
        await state.set_state(BroadcastState.question)
        await message.answer("Напиши свой вопрос, он будет отправлен анонимно")
