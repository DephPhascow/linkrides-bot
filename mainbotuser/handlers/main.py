from aiogram import flags
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from filters.is_admin import IsAdminFilter
from graphql.mutations import run_get_password_or_create
from loaders import main_bot_router
from mainbotuser.keyboards.reply_kb import get_langs
from mainbotuser.states import LanguageState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

@main_bot_router.message(Command("get_my_password"), IsAdminFilter())
@flags.rate_limit(key="get_my_password")
async def on_start(message: Message):
    password = await run_get_password_or_create(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    await message.answer(f"Ваш новый пароль: `{password}`")
    
@main_bot_router.message(Command("start"))
@flags.rate_limit(key="on_start")
async def on_start(message: Message, state: FSMContext, command: CommandObject):
    args: str = command.args
    if args:
        pass
    await message.answer(_("Добро пожаловать!"), reply_markup=get_langs())
    await state.set_state(LanguageState.select)



# @main_bot_router.message(StateFilter(TestState.test), ContentFilter(['text']))
# @flags.rate_limit(key="state-test")
# async def on_deposit_amount(message: Message, state: FSMContext, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
#         await message.answer("Test state")
        
# @main_bot_router.callback_query(TestCallbackData.filter())
# @flags.rate_limit(key="on-select-service-photo")
# async def on_start(query: CallbackQuery, state: FSMContext, callback_data: TestCallbackData, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
#         await query.answer("Test callback", show_alert=True)
        
# @main_bot_router.callback_query(F.data == "my_channels", IsAdminFilter())
# @flags.rate_limit(key="on-select-category-image2video")
# async def on_start(query: CallbackQuery, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
#         await query.message.answer("Test callback for admin", reply_markup=inline_kb_test())

    
# @main_bot_router.message(F.text == 'test')
# @flags.rate_limit(key="on_create_bot")
# async def on_start(message: Message, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#         await message.answer("test", )