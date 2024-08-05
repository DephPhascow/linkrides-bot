from aiogram import Bot, flags, F
from aiogram.types import Message, CallbackQuery
from graphql.enums import TopEnum
from graphql.queres import run_get_top
from loaders import main_bot_router
from mainbotuser.keyboards.inline import type_ratings_kb
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.chat_action import ChatActionSender
    
@main_bot_router.message(F.text == __("🌟 Рейтинг"))
@flags.rate_limit(key="on_select_ratings")
async def on_start(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await state.clear()
        await message.answer(_("Выберите вариант"), reply_markup=type_ratings_kb(None))
        
@main_bot_router.callback_query(F.data == "rating-clients")
@flags.rate_limit(key="on_select_rating_clients")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        top = await run_get_top(query.from_user.id, TopEnum.PASSENGER)
        text = "🌟 *Рейтинг по клиентам*\n"
        text += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balls:,.2f}" for i in range(len(top))])
        await query.message.edit_text(text, reply_markup=type_ratings_kb(TopEnum.PASSENGER))
        
@main_bot_router.callback_query(F.data == "rating-drivers")
@flags.rate_limit(key="on_select_rating_drivers")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        top = await run_get_top(query.from_user.id, TopEnum.TAXI)
        text = "🌟 *Рейтинг по водителям*\n"
        text += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balls:,.2f}" for i in range(len(top))])
        await query.message.edit_text(text, reply_markup=type_ratings_kb(TopEnum.TAXI))
        
@main_bot_router.callback_query(F.data == "rating-all")
@flags.rate_limit(key="on_select_rating_all")
async def on_start(query: CallbackQuery, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=query.from_user.id):
        top = await run_get_top(query.from_user.id, TopEnum.ALL)
        text = "🌟 *Рейтинг по всем*\n"
        text += "\n".join([f"{i + 1}. {top[i].name} - {top[i].balls:,.2f}" for i in range(len(top))])
        await query.message.edit_text(text, reply_markup=type_ratings_kb(TopEnum.ALL))