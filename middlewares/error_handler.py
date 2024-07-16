from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from aiolimiter import AsyncLimiter
from constants import ERROR_CHANNEL, BOT_TOKEN
import traceback

class ErrorHandler(BaseMiddleware):
    def __init__(self, default_rate: int = 1.6) -> None:
        self.limiters: Dict[str, AsyncLimiter] = {}
        self.default_rate = default_rate

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if ERROR_CHANNEL != "":
            try:
                return await handler(event, data)
            except Exception as e:
                tb = traceback.extract_tb(e.__traceback__)
                async with Bot(BOT_TOKEN).context(auto_close=False) as bot:
                    await bot.send_message(ERROR_CHANNEL, f"File: {tb[-1].filename}\n"
                                        "\r\n".join([f"Line: {x.lineno}\ncode: {x.line}" for x in tb]) + "\n"
                                        f"Error: {e}\n")
        else:
            return await handler(event, data)
