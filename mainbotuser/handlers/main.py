from aiogram import flags
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from filters.is_admin import IsAdminFilter
from graphql.mutations import run_get_password_or_create
from loaders import main_bot_router
from mainbotuser.keyboards.reply_kb import get_langs
from mainbotuser.states import RegistrationState
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
        referrer_id = int(args)
        await state.update_data(referrer_id=referrer_id)
    await message.answer(_("Добро пожаловать!"), reply_markup=get_langs())
    await state.set_state(RegistrationState.select_language)