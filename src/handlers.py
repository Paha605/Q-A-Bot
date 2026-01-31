import asyncio

import src.keyboards as kb
from src.db import Database
from src.user_manager import is_admin, admin_list
from aiogram.fsm.context import FSMContext
from src.Sender.broadcast import BroadcastState
from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot
from src.config import TOKEN
import time

router = Router()
db = Database()
bot = Bot(TOKEN)

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    username = message.from_user.username
    user_id = message.from_user.id
    if is_admin(message.from_user.id) == True:
        await message.answer(f"Привет, {message.from_user.full_name}!\nЭтот бот умеет собирать анонимные вопросы, нажмите копку что посмотреть список вопросов", reply_markup=kb.adminkb)

    else:
        await message.answer(f"Привет! Я бот, который помогает задавать анонимные вопросы. Нажми кнопку ниже что бы написать вопрос", reply_markup=kb.main)

@router.message(Command("question"))
@router.message(F.text == "Задать вопрос")
async def replyMsg(message: Message, state: FSMContext):
    await state.set_state(BroadcastState.question)
    await message.answer("Напиши свой вопрос, он будет отправлен анонимно")


@router.message(BroadcastState.question)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)

    if message.text[0] != '/':
        db.add_question(message.date, message.text)
        await message.reply(html.bold("Твой вопрос был отправлен!"))

        # Отправляем сообщение админам через 15 секунд асинхронно
        asyncio.create_task(send_to_admins_after_delay(message.text))

        await state.clear()
    else:
        await state.clear()


async def send_to_admins_after_delay(text: str, delay: int = 15):
    """Отправляет сообщение админам через указанную задержку"""
    await asyncio.sleep(delay)  # Асинхронное ожидание

    for admin in admin_list:
        try:
            await bot.send_message(
                admin,
                "<b>Новый вопрос: </b>" + text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение админу {admin}: {e}")
@router.message()
async def handle_other_messages(message: Message, state: FSMContext) -> None:
    if is_admin(message.from_user.id) == True:
        await message.answer('Что бы посмотреть список вопросов, отправьте -> /question')
    else:
        await message.answer('Что бы задать вопрос, отправьте  -> /question')