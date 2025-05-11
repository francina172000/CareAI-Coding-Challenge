from fastapi import APIRouter
from .endpoints import transcripts

api_router = APIRouter()

api_router.include_router(transcripts.router, prefix = "/transcripts", tags = ["Transcripts"])