from typing import Optional
from aiogram import Bot
from fastapi import BackgroundTasks, APIRouter, Request, Response
import logging
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from loaders import bot_session
from constants import BOT_TOKEN
from geopy.geocoders import Nominatim

from mainbotuser.keyboards.inline import application_taxi_manipulation
from mainbotuser.shortcuts import add_application_message, get_applications

router = APIRouter()
logger = logging.getLogger()

@router.post("/application/new")
async def test(
        request: Request,
        background_tasks: BackgroundTasks,
        taxi_id: int,
        application_id: int,
        from_latitude: float,
        from_longitude: float,
        price: float,
        to_latitude: Optional[float] = None,
        to_longitude: Optional[float] = None,
):
        geolocator = Nominatim(user_agent="linkrides-bot")
        async with Bot(BOT_TOKEN, bot_session, DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)).context(auto_close=False) as bot_:  
                template = """
У Вас новый заказ:
🚖 ID заказа: {application_id}
Забрать из {from_address}
Доставить в {to_address}
Стоимость доставки: {price}                
                """
                msg = await bot_.send_message(taxi_id, template.format(
                        application_id=application_id,
                        from_address=geolocator.reverse(f"{from_latitude}, {from_longitude}").address,
                        to_address=geolocator.reverse(f"{to_latitude}, {to_longitude}").address if to_latitude and to_longitude else "не указано",
                        price=price if to_latitude and to_longitude else str(price) + " за 1 км"
                ), reply_markup=application_taxi_manipulation(application_id))
                await add_application_message(taxi_id, application_id, msg.message_id)
        return Response(status_code=200)

@router.post("/application/delete")
async def test(
        request: Request,
        background_tasks: BackgroundTasks,
        application_id: int,
):
        applications = await get_applications(application_id)
        async with Bot(BOT_TOKEN, bot_session, DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)).context(auto_close=False) as bot_:
                for application in applications:
                        await bot_.delete_message(application.uid, application.message_id)
        return Response(status_code=200)