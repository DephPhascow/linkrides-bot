from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import HOST

def fill_taxi_info():
    btns = InlineKeyboardBuilder()
    HOST = "https://9ac7-202-79-188-146.ngrok-free.app"
    btns.row(
        InlineKeyboardButton(text=f"Заполнить данные", web_app=WebAppInfo(url=f"{HOST}/DriverRegistration"))
    )
    return btns.as_markup()

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
