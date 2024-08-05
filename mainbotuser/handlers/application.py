from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from loaders import main_bot_router
from mainbotuser.callback_datas import ApplicationCallbackData
from mainbotuser.states import RegistrationState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender

    
@main_bot_router.callback_query(ApplicationCallbackData.filter())
@flags.rate_limit(key="on_application")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot, callback_data: ApplicationCallbackData):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        if callback_data.action == "reject":
            await query.answer(_("Вы отклонили заявку"), show_alert=True)
            await query.message.delete()