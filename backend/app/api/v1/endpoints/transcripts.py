from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app import models
from app.core.db import get_db

from app.schemas import transcript as transcript_schema
from app.models import transcript as transcript_model
from app.services import summary_service

router = APIRouter()

@router.post("/", response_model=schemas.transcript.Transcript, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=List[transcript_schema.Transcript])
async def read_transcripts(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all transcripts with pagination.
    Orders by creation date descending (newest first).
    """
    transcripts = (
        db.query(transcript_model.Transcript)
        .order_by(transcript_model.Transcript.created_at.desc()) # Order by newest first
        .offset(skip)
        .limit(limit)
        .all()
    )
    return transcripts

@router.get("/{transcript_id}", response_model=transcript_schema.Transcript)
async def read_transcript(
    transcript_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a single transcript by its ID.
    """
    db_transcript = (
        db.query(transcript_model.Transcript)
        .filter(transcript_model.Transcript.id == transcript_id)
        .first()
    )
    if db_transcript is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return db_transcript

@router.post("/{transcript_id}/resummarize", response_model=transcript_schema.Transcript)
async def resummarize_transcript(
    transcript_id: int,
    background_tasks: BackgroundTasks, # To run summarization in background
    db: Session = Depends(get_db)
):
    """
    Triggers a re-summarization for an existing transcript.
    The actual summarization (and CommLog update) happens in the background.
    """
    db_transcript = db.query(transcript_model.Transcript).filter(transcript_model.Transcript.id == transcript_id).first()
    if not db_transcript:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found")

    # Log the re-run attempt before starting the background task
    try:
        log_entry = transcript_model.CommLog(
            event_type="RESUMMARY_REQUESTED",
            details=f"Re-summarization requested for transcript ID: {transcript_id}",
            transcript_id=transcript_id
        )
        db.add(log_entry)
        db.commit()
        print(f"CommLog: RESUMMARY_REQUESTED event logged for transcript ID: {transcript_id}")
    except Exception as e:
        print(f"Error logging RESUMMARY_REQUESTED to CommLog for transcript {transcript_id}: {e}")
        # db.rollback() # Potentially rollback if logging is critical, though the main task will proceed

    print(f"Transcript ID: {transcript_id} re-summarization requested. Adding to background tasks.")
    background_tasks.add_task(
        summary_service.generate_summary_for_transcript,
        db=db, # Pass the current session (revisit if issues arise with background task sessions)
        transcript_id=transcript_id
    )
    
    db.refresh(db_transcript) 
    return db_transcript

