from typing import List, Optional
from graphql.enums import TopEnum
from graphql.m_types import TariffInfoType, TaxiHistoryType, TopType
from .core.middlewares.auth_middleware import AuthMiddleware
from mainbotuser.shortcuts import get_user
from .core.utils import gen_query
from .settings import gql
from enum import StrEnum

class WhichEnum(StrEnum):
  TAXI = "TAXI"
  PASSENGER = "PASSENGER"


def settings(what_need: str, single: bool = False):
  return gen_query(
    name="settings",
    request=what_need,
    q_words=f"data.settings.{what_need}" if single else f"data.settings",
  )
  
def taxi_history(which: WhichEnum):
  request = "taxi" if which == WhichEnum.TAXI else "passenger"
  return gen_query(
    name="history",
    request=f"fromLatitude, fromLongitude, toLongitude, toLatitude, price, createdAt, {request} {{ firstName, lastName }}",
    to_type=TaxiHistoryType,
    q_words=f"data.history[*].{{ from_latitude: fromLatitude, from_longitude: fromLongitude, to_longitude: toLongitude, to_latitude: toLatitude, price: price, created_at: createdAt, fio: join(' ', [{request}.firstName || '', {request}.lastName || '']) }}",
    var={
      "type": "UserDriveType!"
    }
  )
  
def get_my_taxi_status():
  return gen_query(
    name="me",
    request="getTaxiInfos { status }",
    q_words="data.me.getTaxiInfos.status",
  )
def get_tariffs():
  return gen_query(
    name="tariffs",
    request="id, name, perOneKm",
    to_type=TariffInfoType,
    q_words="data.tariffs[*].{ id: id, name: name, per_one_km: perOneKm }",
  )
  
def get_top():
  return gen_query(
    name="top",
    request="id, firstName, lastName, balls",
    to_type=TopType,
    q_words="data.top[*].{ id: id, name: join(' ', [firstName || 'Не указано', lastName || '']), balls: balls }",
    var={
      "topType": "TopByEnum!"
    }
  )
  

async def run_get_top(tg_id: str, top_type: TopEnum) -> List[TopType]:
  executor = gql.add_query("top", get_top())
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute(variables={
    "topType": top_type.value
  })
  return response['top']

async def run_get_tariffs(tg_id: str) -> List[TariffInfoType]:
  executor = gql.add_query("get_tariffs", get_tariffs())
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute()
  return response['tariffs']

async def run_get_my_taxi_status(tg_id: str) -> Optional[str]:
  executor = gql.add_query("me", get_my_taxi_status())
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute()
  return response['me']

async def run_get_settings(tg_id: str, what_need: str, single: bool) -> any: ### TODO delete
  executor = gql.add_query("settings", settings(what_need, single))
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute()
  return response['settings']

async def run_taxi_history(tg_id: str, type: WhichEnum) -> List[TaxiHistoryType]:
  executor = gql.add_query("settings", taxi_history(type))
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute(variables={
    "type": type.value
  })
  return response['history']