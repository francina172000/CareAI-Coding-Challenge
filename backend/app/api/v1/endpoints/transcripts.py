from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app import models
from app.core.db import get_db

from app.schemas import transcript as transcript_schema
from app.models import transcript as transcript_model
from app.services import summary_service

router = APIRouter()

@router.post("/", response_model=schemas.transcript.Transcript, status_code=201)
async def create_transcript(
    transcript_in: schemas.transcript.TranscriptCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receive a new transcript, store it, log the event, 
    and trigger summarization in the background.
    """
    db_transcript = models.transcript.Transcript(
        original_text = transcript_in.original_text
    )
    db.add(db_transcript)
    db.commit()
    db.refresh(db_transcript)

    try:
        log_entry = transcript_model.CommLog(
            event_type="TRANSCRIPT_CREATED",
            details=f"New transcript received with ID: {db_transcript.id}",
            transcript_id=db_transcript.id
        )
        db.add(log_entry)
        db.commit()
        print(f"CommLog: TRANSCRIPT_CREATED event logged for transcript ID: {db_transcript.id}")
    except Exception as e:
        print(f"Error logging TRANSCRIPT_CREATED to CommLog: {e}")

    print(f"Transcript ID: {db_transcript.id} created. Adding summarization to background tasks.")
    background_tasks.add_task(
        summary_service.generate_summary_for_transcript, 
        db=db,
        transcript_id=db_transcript.id
    )
    
    return db_transcript

