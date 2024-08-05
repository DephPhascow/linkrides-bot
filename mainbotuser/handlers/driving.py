from aiogram import Bot, flags, F
from aiogram.types import Message
from graphql.m_types import DrivingStatus
from graphql.mutations import run_taxi_set_my_location, run_taxi_set_status
from graphql.queres import run_get_my_taxi_status
from loaders import main_bot_router
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters.state import StateFilter
from mainbotuser.keyboards.inline import fill_taxi_info
from mainbotuser.keyboards.reply_kb import cancel, main_panel
from mainbotuser.shortcuts import get_user
from mainbotuser.states import TaxiState

@main_bot_router.message(F.text == __("⛔️ Завершить работу"))
@flags.rate_limit(key="on_select_stop_work")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await run_taxi_set_status(message.from_user.id, DrivingStatus.REST)
        await message.answer(_("Вы закончили работу, чтобы начать новую, нажмите на кнопку 'Начать водить'"), reply_markup=await main_panel(message.from_user.id))        
        
@main_bot_router.message(F.text == __("🚖 Начать водить"))
@flags.rate_limit(key="on_select_find_taxi")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        status = await run_get_my_taxi_status(message.from_user.id)
        match status:
            case None:
                await message.answer(_("Вы еще не заполнили свой профиль, пожалуйста, сперва, заполните его"), reply_markup=fill_taxi_info())
                return 
            case 'REST':
                await message.answer(_("Отправьте ваше live-геолокацию"), reply_markup=cancel())
                await state.set_state(TaxiState.set_my_live_location)
                return
            case _:
                await message.answer(_("Вы уже начали работу, чтобы завершить, нажмите на кнопку 'Завершить работу'"), reply_markup=await main_panel(message.from_user.id))
                return

            
            
@main_bot_router.message(StateFilter(TaxiState.set_my_live_location))
@flags.rate_limit(key="on_select_set_location")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    if message.text == _("❌ Отменить"):
        await state.clear()
        await message.answer(_("Отменено"), reply_markup=await main_panel(message.from_user.id))
        return
    if message.location:
        if not message.location.live_period:
            await message.answer(_("Отправьте ваше live-геолокацию"), reply_markup=cancel())
            return
        try:
            await run_taxi_set_my_location(message.from_user.id, message.location.latitude, message.location.longitude, DrivingStatus.WAIT)
            await message.answer(_("Ваша геолокация успешно установлена, теперь Вы можете ожидать новых клиентов"), reply_markup=await main_panel(message.from_user.id))
        except Exception as e:
            await message.answer(_("Произошла ошибка {error}, попробуйте позже").format(error=f'{e}'), reply_markup=await main_panel(message.from_user.id))