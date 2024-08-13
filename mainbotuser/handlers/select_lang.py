from aiogram import flags
from aiogram.filters import StateFilter
from aiogram.types import Message
from loaders import main_bot_router, i18n
from mainbotuser.keyboards.reply_kb import get_langs, main_panel, send_phone_kb
from mainbotuser.shortcuts import create_user, get_user
from mainbotuser.states import RegistrationState
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

    
@main_bot_router.message(StateFilter(RegistrationState.select_language))
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
    if not user:
        await message.answer(_("Для завершения регистрации, отправьте ваш номер телефона нажав на кнопку ниже"), reply_markup=send_phone_kb())
        await state.set_state(RegistrationState.send_phone_number)
        await state.update_data(language=lang)
        return
    else:
        user.language = lang
        await user.save()
    await state.clear()
    await message.answer(_("Добро пожаловать!"), reply_markup=await main_panel(message.from_user.id))


@main_bot_router.message(StateFilter(RegistrationState.send_phone_number))
@flags.rate_limit(key="on_send_phone_number")
async def on_start(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
        with open("contact.txt", "a", encoding="utf-8") as f:
            f.write(f"{message.contact}\n")
        data = await state.get_data()
        language = data.get("language")
        referrer_id = data.get("referrer_id")
        await create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, language, phone_number, referrer_id)
        await state.clear()
        await message.answer(_("Добро пожаловать!"), reply_markup=await main_panel(message.from_user.id))
    else:
        await message.answer(_("Отправьте свой номер телефона нажав на кнопку ниже"), reply_markup=send_phone_kb())