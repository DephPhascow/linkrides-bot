from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_langs():
    btns = ReplyKeyboardBuilder()
    text = [
        "🇷🇺 Русский",
        "🇺🇿 O'zbek",
        "🇬🇧 English",
    ]
    btns.row(
        *[KeyboardButton(text=i) for i in text],
        width=3,
    )
    return btns.as_markup(resize_keyboard=True)

async def main_panel():
    btns = ReplyKeyboardBuilder()
    text = [
        "🚕 Найти такси",
        "📈 Статистика",
        "👤 Мой профиль",
        "ℹ️ FAQ",
    ]
    btns.row(
        *[KeyboardButton(text=i) for i in text],
        width=2,
    )
    return btns.as_markup(resize_keyboard=True)

def find_taxi(is_from_location: bool):
    btns = ReplyKeyboardBuilder()
    if is_from_location:
        btns.row(
            KeyboardButton(text="📍 Указать текущую позицию", request_location=True),
        )
    else:
        btns.row(
            KeyboardButton(text="✅ Завершить"),
        )
    btns.row(
        KeyboardButton(text="❌ Отмена"),
        width=1,
    )
    return btns.as_markup(resize_keyboard=True)