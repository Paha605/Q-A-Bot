from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Задать вопрос")]], resize_keyboard=True)
adminkb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Смотреть вопросы")]], resize_keyboard=True)
