import logging
import uvicorn
from aiogram import Bot
from fastapi import FastAPI, BackgroundTasks, Body, Response, status
from tortoise import Tortoise
from loaders import dp, close_sessions, bot_session, run_webhook, scheduler
from mainbotuser import main_bot_router
from channels import channel_router
from constants import ALLOWED_HOSTS, BOT_TOKEN, COUNT_WORKERS, LOG_LEVEL, PROJECT_HOST, PROJECT_PORT, TORTOISE_ORM, WEBHOOK_PATH, RUN_JOBS
from contextlib import asynccontextmanager
from api import api_router
from aiogram.client.default import DefaultBotProperties
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_init()
    yield
    await on_shutdown()
    
app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/bot/api")

app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(GZipMiddleware, minimum_size=1000)

async def on_init():
    await run_webhook(BOT_TOKEN)
    await Tortoise.init(
        config=TORTOISE_ORM
    )
    dp.include_router(main_bot_router)
    dp.include_router(channel_router)
    if RUN_JOBS:
        scheduler.start()

async def on_shutdown():
    await Tortoise.close_connections()
    await close_sessions()


async def feed_update(token, update):
    async with Bot(token, bot_session, DefaultBotProperties(parse_mode='markdown')).context(auto_close=False) as bot_:  
        await dp.feed_raw_update(bot_, update)

@app.post(WEBHOOK_PATH, include_in_schema=False)
async def telegram_update(token: str, background_tasks: BackgroundTasks,
                          update: dict = Body(...)) -> Response:
    if token == BOT_TOKEN:
        background_tasks.add_task(feed_update, token, update)
        return Response(status_code=status.HTTP_202_ACCEPTED)
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(
        "main:app",
        host=PROJECT_HOST,
        port=PROJECT_PORT,
        log_level=LOG_LEVEL,
        reload=False,
        access_log=True,
        workers=COUNT_WORKERS,
        timeout_keep_alive=30
    )
