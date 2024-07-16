from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from mainbotuser.callback_datas import TestCallbackData

async def inline_kb_test():
    btns = InlineKeyboardBuilder()
    list = [
        InlineKeyboardButton(text=f"test 1", callback_data="test-1"),
        InlineKeyboardButton(text=f"test 2", callback_data=TestCallbackData(test="test").pack()),
    ]
    btns.row(
        *list,        
        width=1,
    )
    return btns.as_markup()
