from typing import Union
from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from graphql.mutations import run_find_taxi
from graphql.queres import run_get_settings
from loaders import main_bot_router
from mainbotuser.callback_datas import TariffCallbackData
from mainbotuser.keyboards.inline import show_tariffs
from mainbotuser.keyboards.reply_kb import find_taxi, main_panel
from mainbotuser.states import FindTaxiState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calc_distance(from_location, to_location):
    return geodesic(from_location, to_location).kilometers

async def show_text(message: Union[Message, CallbackQuery], state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    message = message.message if isinstance(message, CallbackQuery) else message
    geolocator = Nominatim(user_agent="linkrides-bot")
    text_template = _("*Заказать такси*\n\n"\
        "📍➡️ Из локации: {from_location}\n"\
        "📍⬅️ В локацию: {to_location}\n"\
        "💵 Стоимость: {price} сум\n\n"\
        "{state}")
    data = await state.get_data()
    from_latitude = data.get("from_latitude")
    from_longitude = data.get("from_longitude")
    to_latitude = data.get("to_latitude")
    to_longitude = data.get("to_longitude")
    from_location = to_location = _("Не указано")
    current_position = data.get("current_position", "set_from_address")
    message_id = data.get("message_id")
    if message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
        except:
            pass
    PER_ONE_KM = data.get("price", 0)
    price = PER_ONE_KM #TODO
    if from_latitude and from_longitude:
        from_location = geolocator.reverse(f"{from_latitude}, {from_longitude}").address
    if to_latitude and to_longitude:
        to_location = geolocator.reverse(f"{to_latitude}, {to_longitude}").address
        price = calc_distance((from_latitude, from_longitude), (to_latitude, to_longitude)) * PER_ONE_KM
    text_position = _("Укажите откуда забрать прислав геопозицию") 
    if current_position == "set_to_address":
        text_position = _("Укажите куда доставить прислав геопозицию")
    elif current_position == "confirmation":
        text_position = _("Подтвердите заказ")
    try:
        msg = await message.edit_text(text_template.format(
            from_location = from_location if from_location else _("Не указано"),
            to_location = to_location if to_location else _("Не указано"),
            price = f"{price:,.2f}",
            state = text_position
        ), reply_markup=find_taxi(current_position == "set_from_address"))
    except:
        await message.delete()
        msg = await message.answer(text_template.format(
            from_location = from_location if from_location else _("Не указано"),
            to_location = to_location if to_location else _("Не указано"),
            price = f"{price:,.2f}",
            state = text_position
        ), reply_markup=find_taxi(current_position == "set_from_address"))
    await state.update_data(message_id=msg.message_id)
    
    
@main_bot_router.message(F.text == __("❌ Отмена"), StateFilter(FindTaxiState.set_from_address))
@main_bot_router.message(F.text == __("❌ Отмена"), StateFilter(FindTaxiState.set_to_address))
@main_bot_router.callback_query(F.data == "cancel-find-taxi")
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Union[Message, CallbackQuery], state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = message.from_user.id
    message = message.message if isinstance(message, CallbackQuery) else message
    message_id = data.get("message_id")
    try:
        await message.delete()
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    finally:
        await state.clear()
        await message.answer(_("❌ Отменено"), reply_markup=await main_panel(user_id))
        
    
@main_bot_router.message(F.text == __("🚕 Найти такси"))
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await state.clear()
        await message.answer("Выберите интересующий тариф", reply_markup=await show_tariffs(message.from_user.id))
        
@main_bot_router.callback_query(TariffCallbackData.filter())
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Union[Message, CallbackQuery], state: FSMContext, bot: Bot, callback_data: TariffCallbackData):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        # price = await run_get_settings(message.from_user.id, "costPerKm", True)
        await state.update_data(current_position="set_from_address", price=callback_data.price, tariff_id=callback_data.pk)
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.set_from_address)
        
@main_bot_router.message(StateFilter(FindTaxiState.set_from_address))
@flags.rate_limit(key="on_find_taxi_set_from_address")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        if not message.location:
            await message.answer(_("❌ Отправьте геопозицию"))
            return
        await state.update_data(from_latitude = message.location.latitude, from_longitude = message.location.longitude, current_position="set_to_address")
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.set_to_address)
        
@main_bot_router.message(StateFilter(FindTaxiState.set_to_address))
@flags.rate_limit(key="on_find_taxi_set_to_address")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        if message.text == "✅ Завершить":
            data = await state.get_data()
            from_latitude = data.get("from_latitude")
            from_longitude = data.get("from_longitude")
            tariff_id = data.get("tariff_id")
            try:
                await run_find_taxi(message.from_user.id, tariff_id, from_latitude, from_longitude)
                await message.answer(_("Заказ успешно оформлен"), reply_markup=await main_panel(message.from_user.id))
                await state.clear()
                return
            except Exception as e:
                await message.answer(_("Произошла ошибка {error}, попробуйте позже").format(error=f'{e}'), reply_markup=await main_panel(message.from_user.id))
                await state.clear()
                return
        if not message.location:
            await message.answer(_("❌ Отправьте геопозицию"))
            return
        await state.update_data(to_latitude = message.location.latitude, to_longitude = message.location.longitude, current_position="confirmation")
        await show_text(message, state, bot)
        await state.set_state(FindTaxiState.confirmation)