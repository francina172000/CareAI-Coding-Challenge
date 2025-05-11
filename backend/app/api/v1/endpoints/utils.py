from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text # To execute raw SQL

from app.core.db import get_db, engine # We might need engine directly for some operations
from app.models.transcript import Transcript, CommLog # Import models to know table names

router = APIRouter()

@router.post("/clear-all-data", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_data(db: Session = Depends(get_db)):
    """
    Clears all data from the transcripts and commlog tables and resets their ID sequences.
    USE WITH CAUTION - THIS IS A DESTRUCTIVE OPERATION.
    """
    try:
        # Delete all rows from CommLog first due to foreign key constraint from Transcript
        db.execute(text(f"DELETE FROM {CommLog.__tablename__}"))
        print(f"Cleared all data from {CommLog.__tablename__}")

        # Delete all rows from Transcripts
        db.execute(text(f"DELETE FROM {Transcript.__tablename__}"))
        print(f"Cleared all data from {Transcript.__tablename__}")

        # Reset ID sequences
        # Default sequence names are <table_name>_<pk_column_name>_seq
        db.execute(text(f"ALTER SEQUENCE {CommLog.__tablename__}_id_seq RESTART WITH 1"))
        print(f"Reset ID sequence for {CommLog.__tablename__}")
        
        db.execute(text(f"ALTER SEQUENCE {Transcript.__tablename__}_id_seq RESTART WITH 1"))
        print(f"Reset ID sequence for {Transcript.__tablename__}")

        db.commit()
        print("All data cleared and ID sequences reset successfully.")
        # No content to return, so status_code=204
        return
    
    except Exception as e:
        db.rollback()
        print(f"Error clearing data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while clearing data: {str(e)}"
        )
