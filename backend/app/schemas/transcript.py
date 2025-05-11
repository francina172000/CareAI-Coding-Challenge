from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TranscriptBase(BaseModel):
    original_text: str
    summary_text: Optional[str] = None

class TranscriptCreate(BaseModel):
    original_text: str

class TranscriptUpdate(BaseModel):
    summary_text: Optional[str] = None

class TranscriptInDBBase(TranscriptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Transcript(TranscriptInDBBase):
    pass

class CommLogBase(BaseModel):
    event_type: str
    details: Optional[str] = None
    transcript_id: Optional[int] = None

class CommLogCreate(CommLogBase):
    pass

class CommLogInDBBase(CommLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class CommLog(CommLogInDBBase):
    pass