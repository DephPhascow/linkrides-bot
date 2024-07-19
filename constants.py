from dotenv import load_dotenv
import os
from ast import literal_eval

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
HOST = os.getenv("HOST")
DB_URL=os.getenv("DB_URL")
REDIS = os.getenv("REDIS")
ERROR_CHANNEL = os.getenv("ERROR_CHANNEL")
GRAPHQL_URL = os.getenv("GRAPHQL_URL")
BOT_IN_RECONSTRUCTION = True if os.getenv("BOT_IN_RECONSTRUCTION") == "True" else False
PROJECT_HOST = os.getenv("PROJECT_HOST")
PROJECT_PORT = int(os.getenv("PROJECT_PORT"))
IS_LOCAL_BOT = literal_eval(os.getenv("IS_LOCAL_BOT"))
COUNT_WORKERS = int(os.getenv("COUNT_WORKERS"))
ADMIN = int(os.getenv("ADMIN"))
ADMINS = literal_eval(os.getenv("ADMINS"))
RUN_JOBS = literal_eval(os.getenv("RUN_JOBS"))
DEBUG = literal_eval(os.getenv("DEBUG"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL")
IP_WHITELIST = literal_eval(os.getenv("IP_WHITELIST"))
ALLOWED_HOSTS = literal_eval(os.getenv("ALLOWED_HOSTS"))
ALLOWED_UPDATES = literal_eval(os.getenv("ALLOWED_UPDATES"))
APSHCEDULLER_REDIS_DB_NUMBER = int(os.getenv("APSHCEDULLER_REDIS_DB_NUMBER"))
AIOGRAM_REDIS_DB_NUMBER = int(os.getenv("AIOGRAM_REDIS_DB_NUMBER"))

AIOGRAM_SECRET = os.getenv("AIOGRAM_SECRET")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

ADMIN_LIST = [
    int(ADMIN),
]

CONFIGS = {
    "BOT_ON_RECONSTRUCTION": BOT_IN_RECONSTRUCTION,
}

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["aerich.models", "models"],
            "default_connection": "default",
        },
    },
}
