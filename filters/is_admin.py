from typing import Union
from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from constants import ADMINS

router = Router()


class IsAdminFilter(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.from_user.id in ADMINS