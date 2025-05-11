from fastapi import APIRouter
from .endpoints import transcripts
from .endpoints import commlogs
from .endpoints import utils

api_router = APIRouter()

api_router.include_router(transcripts.router, prefix = "/transcripts", tags = ["Transcripts"])
api_router.include_router(commlogs.router, prefix = "/commlogs", tags = ["CommLogs"])
api_router.include_router(utils.router, prefix = "/utils", tags = ["Utilities"])