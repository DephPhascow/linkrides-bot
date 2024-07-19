from aiogram import flags
from aiogram.filters import StateFilter
from aiogram.types import Message
from loaders import main_bot_router, i18n
from mainbotuser.keyboards.reply_kb import get_langs, main_panel
from mainbotuser.shortcuts import create_user, get_user
from mainbotuser.states import LanguageState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

    
@main_bot_router.message(StateFilter(LanguageState.select))
@flags.rate_limit(key="on_select_lang_ru")
async def on_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = message.from_user.language_code
    match message.text:
        case "🇷🇺 Русский":
            lang = "ru"
        case "🇬🇧 English":
            lang = "en"
        case "🇺🇿 O'zbek":
            lang = "uz"
        case _:
            await message.answer("Выберите язык!", reply_markup=get_langs())
            return
    i18n.ctx_locale.set(lang)
    await state.clear()
    if not user:
        await create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, lang=lang)
    else:
        user.language = lang
        await user.save()
    await message.answer(_("Добро пожаловать!"), reply_markup=await main_panel())
