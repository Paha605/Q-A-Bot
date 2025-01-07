import src.keyboards as kb
from src.db import Database
from src.user_manager import is_admin
from aiogram.fsm.context import FSMContext
from src.Sender.broadcast import BroadcastState
from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot
from src.config import TOKEN

router = Router()
db = Database()
bot = Bot(TOKEN)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    username = message.from_user.username
    user_id = message.from_user.id
    if is_admin(message.from_user.id) == True:
        await message.answer(f"Привет, {message.from_user.full_name}!\nЭтот бот умеет собирать анонимные вопросы, нажимай ", reply_markup=kb.adminkb)

    else:
        await message.answer(f"Привет, {message.from_user.full_name}!\nЭтот бот умеет собирать анонимные вопросы, нажимай на кнопку если хочешь задать вопрос", reply_markup=kb.main)


@router.message(F.text == "Задать вопрос")
async def replyMsg(message: Message, state: FSMContext):
    await state.set_state(BroadcastState.question)
    await message.answer("Напиши свой вопрос, он будет отправлен анонимно")

@router.message(BroadcastState.question)
async def process_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    db.add_question(message.date, message.text)
    await message.reply(html.bold("Твой вопрос был отправлен!"))
    await bot.send_message(1267019026, "<b>Новый вопрос: </b>" + message.text, parse_mode="HTML")
    await state.clear()