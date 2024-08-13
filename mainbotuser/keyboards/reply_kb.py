from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from graphql.queres import run_get_my_taxi_status

def cancel():
    btns = ReplyKeyboardBuilder()
    btns.row(
        KeyboardButton(text=_("❌ Отменить"), ),
        width=1,
    )
    return btns.as_markup(resize_keyboard=True)

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

async def main_panel(user_id: str):
    btns = ReplyKeyboardBuilder()
    status = await run_get_my_taxi_status(user_id)
    text = _("🚖 Начать водить") if not status or status == "REST" else _("⛔️ Завершить работу")
    text = [
        _("🚕 Найти такси"),
        text,
        _("👤 Реферальная система"),
        _("🌟 Рейтинг"),
        _("📈 Статистика"),
        _("👤 Мой профиль"),
        _("ℹ️ FAQ"),
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
            KeyboardButton(text=_("📍 Указать текущую позицию"), request_location=True),
        )
    else:
        btns.row(
            KeyboardButton(text=_("✅ Завершить")),
        )
    btns.row(
        KeyboardButton(text=_("❌ Отмена")),
        width=1,
    )
    return btns.as_markup(resize_keyboard=True)

def send_phone_kb():
    btns = ReplyKeyboardBuilder()
    btns.row(
        KeyboardButton(text=_("Отправить номер телефона"), request_contact=True),
        width=1,
    )
    return btns.as_markup(resize_keyboard=True)