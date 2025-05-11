from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key = True, index = True)
    original_text = Column(Text, nullable = False)
    summary_text = Column(Text, nullable = True)

    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), default = func.now(), onupdate = func.now())

    # Relationship: A Transcript can have many CommLog entries
    # 'cascade="all, delete-orphan"' means if a Transcript is deleted, its logs are also deleted.
    logs = relationship("CommLog", back_populates="transcript", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Transcript(id={self.id}, summary_present={self.summary_text is not None})>"
    
class CommLog(Base):
     __tablename__ = "commlog"

     id = Column(Integer, primary_key=True, index=True)
     event_type = Column(String(100), nullable=False)
     details = Column(Text, nullable=True)
     transcript_id = Column(Integer, ForeignKey("transcripts.id"), nullable=True) 
     timestamp = Column(DateTime(timezone=True), server_default=func.now())

     # Relationship: A CommLog entry belongs to one Transcript
     transcript = relationship("Transcript", back_populates="logs")

     def __repr__(self):
         return f"<CommLog(id={self.id}, event_type='{self.event_type}')>"

