from typing import Optional
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from constants import HOST
from graphql.enums import TopEnum
from graphql.queres import run_get_my_taxi_status, run_get_tariffs
from mainbotuser.callback_datas import ApplicationCallbackData, TariffCallbackData

def send_my_phone_number(application_id: int):
    btns = InlineKeyboardBuilder()
    btns.row(
        InlineKeyboardButton(text=f"Предоставить номер телефона", callback_data="set_my_phone")
        # InlineKeyboardButton(text=_(f"Предоставить номер телефона"), callback_data="set_my_phone")
    )
    return btns.as_markup()

def fill_taxi_info():
    btns = InlineKeyboardBuilder()
    btns.row(
        InlineKeyboardButton(text=_(f"Заполнить данные"), web_app=WebAppInfo(url=f"{HOST}/DriverRegistration"))
    )
    return btns.as_markup()

async def profile_kb(user_id: str):
    btns = InlineKeyboardBuilder()
    list = [
        InlineKeyboardButton(text=_(f"🚕 История поездок"), callback_data="history"),
    ]
    status = await run_get_my_taxi_status(user_id)
    if status:
        list.append(InlineKeyboardButton(text=_(f"🚖 Мои доставки"), callback_data="my-work"))
    btns.row(
        *list,        
        width=1,
    )
    return btns.as_markup()

async def show_tariffs(user_id: int):
    btns = InlineKeyboardBuilder()
    tariffs = await run_get_tariffs(user_id)
    list = [
        InlineKeyboardButton(text=f'{tariff.name} ({tariff.per_one_km} сум)', callback_data=TariffCallbackData(pk=tariff.id, price=tariff.per_one_km).pack()) for tariff in tariffs
    ]
    list.append(InlineKeyboardButton(text=_(f"❌ Отменить"), callback_data="cancel-find-taxi")) ### TODO 
    btns.row(
        *list,        
        width=1,
    )
    return btns.as_markup()

def application_taxi_manipulation(application_id: int):
    btns = InlineKeyboardBuilder()
    btns.row(
        InlineKeyboardButton(text="Отклонить", callback_data=ApplicationCallbackData(action="reject", pk=application_id).pack()),
        InlineKeyboardButton(text="Принять", callback_data=ApplicationCallbackData(action="accept", pk=application_id).pack()),
        #TODO эти кнопки выводятся в API там нет i18n надо там настроить
        # InlineKeyboardButton(text=_("Отклонить"), callback_data=ApplicationCallbackData(action="reject", pk=application_id).pack()),
        # InlineKeyboardButton(text=_("Принять"), callback_data=ApplicationCallbackData(action="accept", pk=application_id).pack()),
        width=1,
    )
    return btns.as_markup()

def type_ratings_kb(current_top_type: Optional[TopEnum] = None):
    keyboards = InlineKeyboardBuilder()
    btns = []
    if current_top_type != TopEnum.PASSENGER:
        btns.append(InlineKeyboardButton(text=_("Рейтинг по клиентам"), callback_data="rating-clients"))
    if current_top_type != TopEnum.TAXI:
        btns.append(InlineKeyboardButton(text=_("Рейтинг по таксистам"), callback_data="rating-drivers"))
    if current_top_type != TopEnum.ALL:
        btns.append(InlineKeyboardButton(text=_("Общий рейтинг"), callback_data="rating-all"))
    keyboards.row(
        *btns,
        width=1,
    )
    return keyboards.as_markup()
