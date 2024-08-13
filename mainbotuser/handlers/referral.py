from aiogram import Bot, flags, F
from aiogram.types import Message
from loaders import main_bot_router
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
    
@main_bot_router.message(F.text == __("👤 Реферальная система"))
@flags.rate_limit(key="on_select_ratings")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await state.clear()
        me = await bot.get_me()
        await message.answer(
            _("Приглашайте клиентов, чтобы зарабатывать балы\nВаша ссылка для приглашения: {url}").format(
                url = f"https://t.me/{me.username}?start={message.from_user.id}"
            ),
        )