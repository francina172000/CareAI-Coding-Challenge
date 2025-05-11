from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app import models
from app.core.db import get_db

from app.schemas import transcript as transcript_schema

router = APIRouter()

@router.post("/", response_model=schemas.transcript.Transcript, status_code=201)
async def create_transcript(
    transcript_in: schemas.transcript.TranscriptCreate,
    db: Session = Depends(get_db)
):
    """
    Receive a new transcript, store it, and eventually trigger summarization.
    For now, it just stores the original transcript.
    """
    db_transcript = models.transcript.Transcript(
        original_text=transcript_in.original_text
    )
    db.add(db_transcript)
    db.commit()
    db.refresh(db_transcript)
    return db_transcript

