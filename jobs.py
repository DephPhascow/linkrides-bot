import logging
from apscheduler.triggers.cron import CronTrigger
from aiogram.utils.i18n import gettext as _
from loaders import scheduler
logger = logging.getLogger()

async def clear_statistics():
    pass
    
scheduler.add_job(clear_statistics, trigger=CronTrigger(hour=0, minute=0, second=0))