from typing import List, Optional
from graphql.m_types import TaxiHistoryType
from .core.middlewares.auth_middleware import AuthMiddleware
from mainbotuser.shortcuts import get_user
from .core.utils import gen_query
from .settings import gql

def settings(what_need: str, single: bool = False):
  return gen_query(
    name="settings",
    request=what_need,
    q_words=f"data.settings.{what_need}" if single else f"data.settings",
  )
  
def taxi_history():
  return gen_query(
    name="history",
    request="fromLatitude, fromLongitude, toLongitude, toLatitude, price, createdAt, taxi { user { firstName, lastName } }",
    to_type=TaxiHistoryType,
    q_words="data.history[*].{ from_latitude: fromLatitude, from_longitude: fromLongitude, to_longitude: toLongitude, to_latitude: toLatitude, price: price, created_at: createdAt, taxi_fio: join(' ', [taxi.user.firstName, taxi.user.lastName || '']) }",
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
  

async def run_get_my_taxi_status(tg_id: str) -> Optional[str]:
  executor = gql.add_query("me", get_my_taxi_status())
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute()
  return response['me']

async def run_get_settings(tg_id: str, what_need: str, single: bool) -> any:
  executor = gql.add_query("settings", settings(what_need, single))
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute()
  return response['settings']

async def run_taxi_history(tg_id: str, type: str) -> List[TaxiHistoryType]:
  executor = gql.add_query("settings", taxi_history())
  user = await get_user(tg_id)
  auth: AuthMiddleware = executor['middleware__auth']
  await auth.set_data(f'{user.uid}', user.password, user.jwt_token, user.jwt_token_exp, user.jwt_refresh_token, user.jwt_refresh_token_exp)
  response = await executor.execute(variables={
    "type": type
  })
  return response['history']