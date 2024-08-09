from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from graphql.queres import WhichEnum, run_taxi_history
from loaders import main_bot_router
from mainbotuser.keyboards.inline import profile_kb
from mainbotuser.states import RegistrationState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
from geopy.geocoders import Nominatim
    
@main_bot_router.message(F.text == __("👤 Мой профиль"))
@flags.rate_limit(key="on_select_profile")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await message.answer(_("Ваш профиль"), reply_markup=await profile_kb(message.from_user.id))

async def generator_text(user_id: int, which: WhichEnum):
    history = await run_taxi_history(user_id, which)
    name = "🚖 Водитель" if which == WhichEnum.PASSENGER else "👤 Пассажир"
    template = _(
        "📍➡️ Откуда: {from_}\r\n"\
        "📍⬅️ Куда: {to}\r\n"\
        "📅 Дата: {date}\r\n"\
        "💲 цена: {price}\r\n"\
        "{name}: {driver}\r\n"\
    )
    text = [
        template.format(
            from_ = x.from_address,
            to = x.to_address,
            date = x.created_at.strftime("%d.%m.%Y %H:%M"),
            price = f"{x.price:,.2f}",
            driver = x.fio,
            name = name
        ) for x in history
    ]
    return text
        
@main_bot_router.callback_query(F.data == "history")
@flags.rate_limit(key="on_select_history")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        text = await generator_text(query.from_user.id, WhichEnum.PASSENGER)
        if len(text) == 0:
            text = _("История пуста")
        await query.message.edit_text(_("*История поездок*\n\n{text}").format(text="\r\n".join(text)), reply_markup=await profile_kb(query.from_user.id))


@main_bot_router.callback_query(F.data == "my-work")
@flags.rate_limit(key="on_my-work")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        text = await generator_text(query.from_user.id, WhichEnum.TAXI)
        await query.message.edit_text(_("*История поездок*\n\n{text}").format(text="\r\n".join(text)), reply_markup=await profile_kb(query.from_user.id))