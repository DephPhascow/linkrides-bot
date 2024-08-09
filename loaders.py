from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio.client import Redis
from constants import AIOGRAM_REDIS_DB_NUMBER, AIOGRAM_SECRET, ALLOWED_UPDATES, APSHCEDULLER_REDIS_DB_NUMBER, BOT_TOKEN, IS_LOCAL_BOT, REDIS, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, WEBHOOK_URL
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from filters.chat_filter import ChatTypeFilter
from middlewares.bot_reconstruction import BotInReconstruction
from middlewares.error_handler import ErrorHandler
from middlewares.language_middleware import LanguageMiddleware
from middlewares.trottling import ThrottlingMiddleware
from middlewares.user_data import UserDataMiddleware
from aiogram.types import BotCommand
from aiogram.exceptions import TelegramUnauthorizedError
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

async def delete_webhook(bot_token: str):
    async with Bot(bot_token, bot_session).context(auto_close=False) as bot_:
        await bot_.delete_webhook()

async def run_webhook(bot_token: str):
    webhook_url = WEBHOOK_URL.format(token=bot_token)
    try:
        async with Bot(bot_token, bot_session, DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)).context(auto_close=False) as bot_:  
            webhook_info = await bot_.get_webhook_info()
            # if webhook_info.url != webhook_url or webhook_info.allowed_updates != ALLOWED_UPDATES:
            await bot_.set_webhook(
                webhook_url,
                allowed_updates=ALLOWED_UPDATES,
                drop_pending_updates=False,
                secret_token=AIOGRAM_SECRET,
            )
            commands = await bot_.get_my_commands()
            bot_commands = [
                BotCommand(command="/start", description="Начать использование"),
            ]
            if bot_commands != commands:
                await bot_.set_my_commands(bot_commands)
    except TelegramUnauthorizedError as e:
        pass
    


redis = None
if not IS_LOCAL_BOT:
    redis = Redis.from_url(url=REDIS, db=AIOGRAM_REDIS_DB_NUMBER)
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_bot_id=True))
else:
    storage = MemoryStorage()

dp = Dispatcher(
    storage=storage,
    fsm_strategy=FSMStrategy.USER_IN_CHAT
)

bot_session = AiohttpSession()
main_bot = Bot(
    BOT_TOKEN,
    session=bot_session,
    default=DefaultBotProperties(
        parse_mode="Markdown"
    )
)

main_bot_router = Router(name="mainbot")
main_bot_router.message.filter(
    ChatTypeFilter(chat_type=["private"])
)
main_bot_router.callback_query.filter(
    ChatTypeFilter(chat_type=["private"])
)
channel_router = Router(name="channel_router")
channel_router.message.filter(
    ChatTypeFilter(chat_type=["channel"]),
)
channel_router.callback_query.filter(
    ChatTypeFilter(chat_type=["channel"]),
)

for middleware in [
    ThrottlingMiddleware(),
    BotInReconstruction(),
    UserDataMiddleware(),
    ErrorHandler(),
]:
    dp.message.middleware(middleware)
    dp.callback_query.middleware(middleware)
    
i18n = I18n(path="locales", default_locale="ru", domain="messages")
a = LanguageMiddleware(i18n)
a.setup(dp)

async def close_sessions():
    if not IS_LOCAL_BOT:
        await redis.close()
    await dp.storage.close()

storage = MemoryJobStore()
if not IS_LOCAL_BOT:
    storage = RedisJobStore(db=APSHCEDULLER_REDIS_DB_NUMBER, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
scheduler = AsyncIOScheduler(
    jobstores={
        'default': storage
    },
    executors={
        'default': AsyncIOExecutor(),
        'processpool': ProcessPoolExecutor(max_workers=1)
    },
    job_defaults={
            'misfire_grace_time': 15 * 60,
            "coalesce": False,
            "max_instances": 1,
        }
)
