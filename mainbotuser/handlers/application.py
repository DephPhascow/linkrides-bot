from aiogram import Bot, flags
from aiogram.types import CallbackQuery
from graphql.core.models import Errors
from graphql.mutations import run_taxi_accept_application, run_taxi_cancel_application
from loaders import main_bot_router
from mainbotuser.callback_datas import ApplicationCallbackData
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender

    
@main_bot_router.callback_query(ApplicationCallbackData.filter())
@flags.rate_limit(key="on_application")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot, callback_data: ApplicationCallbackData):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        if callback_data.action == "reject":
            try:
                await run_taxi_cancel_application(query.from_user.id, callback_data.pk)
                await query.answer(_("Вы отклонили заявку"), show_alert=True)
                await query.message.delete()
            except Errors as e:
                await query.answer("\n".join([x.message for x in e.errors]), show_alert=True)
        elif callback_data.action == "accept":
            try:
                await run_taxi_accept_application(query.from_user.id, callback_data.pk)
                await query.answer(_("Вы приняли заявку"), show_alert=True)
                await query.message.delete()
            except Errors as e:
                await query.answer("\n".join([x.message for x in e.errors]), show_alert=True)