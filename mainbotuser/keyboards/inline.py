from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def profile_kb():
    btns = InlineKeyboardBuilder()
    list = [
        InlineKeyboardButton(text=f"🚕 История поездок", callback_data="history"),
    ]
    btns.row(
        *list,        
        width=2,
    )
    return btns.as_markup()
