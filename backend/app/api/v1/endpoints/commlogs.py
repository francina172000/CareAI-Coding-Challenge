from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import transcript as transcript_schema # CommLog schemas are in transcript.py
from app.models import transcript as transcript_model # CommLog model is in transcript.py
from app.core.db import get_db

router = APIRouter()

@router.get("/", response_model=List[transcript_schema.CommLog])
async def read_commlogs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all commlog entries with pagination.
    Orders by timestamp descending (newest first).
    """
    commlogs = (
        db.query(transcript_model.CommLog)
        .order_by(transcript_model.CommLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return commlogs

@router.get("/transcript/{transcript_id}", response_model=List[transcript_schema.CommLog])
async def read_commlogs_for_transcript(
    transcript_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve commlog entries for a specific transcript with pagination.
    Orders by timestamp descending (newest first).
    """
    # First, check if the transcript exists (optional, but good practice)
    transcript = db.query(transcript_model.Transcript).filter(transcript_model.Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail=f"Transcript with id {transcript_id} not found.")

    commlogs = (
        db.query(transcript_model.CommLog)
        .filter(transcript_model.CommLog.transcript_id == transcript_id)
        .order_by(transcript_model.CommLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return commlogs
