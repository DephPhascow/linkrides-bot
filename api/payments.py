from fastapi import BackgroundTasks, APIRouter, Request
import logging
from fastapi import BackgroundTasks, APIRouter, Request


router = APIRouter()
logger = logging.getLogger()

@router.post("/test/")
async def test(
        request: Request,
        background_tasks: BackgroundTasks,
):
        data = request.data
        pass