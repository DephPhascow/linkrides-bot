from aiogram import flags
from aiogram.types import CallbackQuery
from loaders import channel_router



@channel_router.callback_query(F.data == "test")
@flags.rate_limit(key="on_start")
async def on_start(query: CallbackQuery, ):
    pass