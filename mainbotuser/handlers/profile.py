from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from graphql.queres import run_taxi_history
from loaders import main_bot_router
from mainbotuser.keyboards.inline import profile_kb
from mainbotuser.states import LanguageState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
from geopy.geocoders import Nominatim
    
@main_bot_router.message(F.text == __("👤 Мой профиль"))
@flags.rate_limit(key="on_select_profile")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await message.answer(_("Ваш профиль"), reply_markup=await profile_kb())
        
@main_bot_router.callback_query(F.data == "history")
@flags.rate_limit(key="on_select_history")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    geolocator = Nominatim(user_agent="linkrides-bot")
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        history = await run_taxi_history(query.from_user.id, "PASSENGER")
        print(history)
        template = _(
            "📍➡️ Откуда: {from_}\r\n"\
            "📍⬅️ Куда: {to}\r\n"\
            "📅 Дата: {date}\r\n"\
            "💲 цена: {price}\r\n"\
            "🚖 Водитель: {driver}\r\n"\
        )
        text = [
            template.format(
                from_ = geolocator.reverse(f"{x.from_latitude}, {x.from_longitude}").address,
                to = geolocator.reverse(f"{x.to_latitude}, {x.to_longitude}").address,
                date = x.created_at.strftime("%d.%m.%Y %H:%M"),
                price = f"{x.price:,.2f}",
                driver = x.taxi_fio
            ) for x in history
        ]
        await query.message.edit_text(_("*История поездок*\n\n{text}").format(text="\r\n".join(text)), reply_markup=await profile_kb())