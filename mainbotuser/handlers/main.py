from aiogram import Bot, flags, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message, CallbackQuery
from filters.content_filter import ContentFilter
from filters.is_admin import IsAdminFilter
from loaders import main_bot_router
from mainbotuser.callback_datas import TestCallbackData
from mainbotuser.keyboards.inline import inline_kb_test
from mainbotuser.keyboards.reply_kb import reply_kb_test
from mainbotuser.states import TestState
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext


@main_bot_router.message(StateFilter(TestState.test), ContentFilter(['text']))
@flags.rate_limit(key="state-test")
async def on_deposit_amount(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await message.answer("Test state")
        
@main_bot_router.callback_query(TestCallbackData.filter())
@flags.rate_limit(key="on-select-service-photo")
async def on_start(query: CallbackQuery, state: FSMContext, callback_data: TestCallbackData, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        await query.answer("Test callback", show_alert=True)
        
@main_bot_router.callback_query(F.data == "my_channels", IsAdminFilter())
@flags.rate_limit(key="on-select-category-image2video")
async def on_start(query: CallbackQuery, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        await query.message.answer("Test callback for admin", reply_markup=inline_kb_test())

@main_bot_router.message(Command("start"), StateFilter(None))
@flags.rate_limit(key="on_start")
async def on_start(message: Message, bot: Bot, command: CommandObject):
    args: str = command.args
    if args:
        pass
    await message.answer("test")
    
@main_bot_router.message(F.text == 'test')
@flags.rate_limit(key="on_create_bot")
async def on_start(message: Message, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer("test", )