from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from graphql.queres import run_get_settings
from loaders import main_bot_router
from mainbotuser.keyboards.reply_kb import find_taxi
from mainbotuser.states import FindTaxiState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calc_distance(from_location, to_location):
    return geodesic(from_location, to_location).kilometers

async def show_text(message: Message, state: FSMContext, bot: Bot):
    geolocator = Nominatim(user_agent="linkrides-bot")
    text_template = _("*Заказать такси*\n\n"\
        "📍➡️ Из локации: {from_location}\n"\
        "📍⬅️ В локацию: {to_location}\n"\
        "💵 Стоимость: {price} сум\n\n"\
        "{state}")
    data = await state.get_data()
    from_location = data.get("from_location")
    to_location = data.get("to_location")
    current_position = data.get("current_position", "set_from_address")
    message_id = data.get("message_id")
    if message_id:
        try:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
        except:
            pass
    PER_ONE_KM = data.get("price", 0)
    price = PER_ONE_KM #TODO
    if to_location:
        a = from_location.split("x")
        b = to_location.split("x")
        price = calc_distance(a, b) * PER_ONE_KM
    if from_location:
        from_location = from_location.split("x")
        from_location = geolocator.reverse(f"{from_location[0]}, {from_location[1]}").address
    if to_location:
        to_location = to_location.split("x")
        to_location = geolocator.reverse(f"{to_location[0]}, {to_location[1]}").address
    text_position = _("Укажите откуда забрать прислав геопозицию") 
    if current_position == "set_to_address":
        text_position = _("Укажите куда доставить прислав геопозицию")
    elif current_position == "confirmation":
        text_position = _("Подтвердите заказ")
    msg = await message.answer(text_template.format(
        from_location = from_location if from_location else _("Не указано"),
        to_location = to_location if to_location else _("Не указано"),
        price = f"{price:,.2f}",
        state = text_position
    ), reply_markup=find_taxi(current_position == "set_from_address"))
    await state.update_data(message_id=msg.message_id)
    
    
@main_bot_router.message(F.text == __("❌ Отмена"), StateFilter(FindTaxiState.set_from_address))
@main_bot_router.message(F.text == __("❌ Отмена"), StateFilter(FindTaxiState.set_to_address))
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    finally:
        await state.clear()
        await message.answer(_("❌ Отменено"))
        
    
@main_bot_router.message(F.text == __("🚕 Найти такси"))
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        price = await run_get_settings(message.from_user.id, "costPerKm", True)
        await state.update_data(current_position="set_to_address", price=price)
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.set_from_address)
        await state.update_data(current_position="set_to_address")
        
@main_bot_router.message(StateFilter(FindTaxiState.set_from_address))
@flags.rate_limit(key="on_find_taxi_set_from_address")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        if not message.location:
            await message.answer(_("❌ Отправьте геопозицию"))
            return
        await state.update_data(from_location = f'{message.location.latitude}x{message.location.longitude}')
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.set_to_address)
        await state.update_data(current_position="confirmation")
        
@main_bot_router.message(StateFilter(FindTaxiState.set_to_address))
@flags.rate_limit(key="on_find_taxi_set_to_address")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        if message.text == "✅ Завершить":
            pass #TODO
        if not message.location:
            await message.answer(_("❌ Отправьте геопозицию"))
            return
        await state.update_data(to_location = f'{message.location.latitude}x{message.location.longitude}')
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.confirmation)
        await state.update_data(current_position="confirmation")