from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def reply_kb_test():
    btns = ReplyKeyboardBuilder()
    text = [
        "test",
    ]
    btns.row(
        *[KeyboardButton(text=i) for i in text],
        width=2
    )
    return btns.as_markup(resize_keyboard=True)