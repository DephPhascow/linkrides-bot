from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiolimiter import AsyncLimiter
from constants import ADMIN_LIST, CONFIGS


class BotInReconstruction(BaseMiddleware):
    def __init__(self, default_rate: int = 1.6) -> None:
        self.limiters: Dict[str, AsyncLimiter] = {}
        self.default_rate = default_rate

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if CONFIGS['BOT_ON_RECONSTRUCTION'] and event.from_user.id not in ADMIN_LIST:
            await event.answer("Бот временно на реконструкции")
            return
        return await handler(event, data)
        
