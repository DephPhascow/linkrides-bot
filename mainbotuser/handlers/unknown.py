from aiogram import Bot, flags
from aiogram.types import Message, ChatMemberUpdated
from loaders import main_bot_router
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.utils.i18n import gettext as _

@main_bot_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated, bot: Bot):
    pass


@main_bot_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, bot: Bot):
    pass

@main_bot_router.message()
@flags.rate_limit(key="on_any")
async def on_start(message: Message, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(_("Я Вас не понял 😔\nНажмите на /start чтобы получить список команд"), )