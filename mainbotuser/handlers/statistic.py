from aiogram import Bot, flags, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from loaders import main_bot_router
from mainbotuser.states import LanguageState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender

    
@main_bot_router.message(F.text == __("📈 Статистика"))
@flags.rate_limit(key="on_select_statistic")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await message.answer(_("Пока не реализованно"))