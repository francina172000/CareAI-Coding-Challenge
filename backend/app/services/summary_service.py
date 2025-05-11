import google.generativeai as genai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.transcript import Transcript
from app.models.transcript import CommLog
from app.schemas.transcript import TranscriptUpdate

try:
    genai.configure(api_key = settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini: {e}. Summarization might not work as expected!")

try:
    model_name_to_try = 'gemini-2.5-flash-preview-04-17' 
    print(f"Attempting to initialize Gemini model: {model_name_to_try}")
    model = genai.GenerativeModel(model_name_to_try)
    print(f"Successfully initialized Gemini model: {model_name_to_try}")
except Exception as e:
    print(f"Error initializing Gemini model '{model_name_to_try}': {e}. Summarization might not work.")
    model = None

def _log_to_commlog(db_session: Session, transcript_id: int, event_type: str, details: str | None = None):
    """Helper function to add entries to CommLog."""
    try:
        log_entry = CommLog(
            transcript_id=transcript_id,
            event_type=event_type,
            details=details
        )
        db_session.add(log_entry)
        db_session.commit()
        print(f"CommLog: {event_type} event logged for transcript ID: {transcript_id}")
    except Exception as e:
        print(f"Error logging {event_type} to CommLog for transcript {transcript_id}: {e}")
        db_session.rollback() # Rollback this specific log attempt if it fails

async def generate_summary_for_transcript(db: Session, transcript_id: int) -> Transcript | None:
    """
    Fetch a transcript, generate summary using Gemini API
    Return updated transcript if obtained successfully, else return None
    """
    if not model:
        print("Gemini model not initialized. Skipping summarization.")
        _log_to_commlog(db, transcript_id, "SUMMARY_SKIPPED", "Gemini model not initialized.")
        return None
    
    db_transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not db_transcript:
        print(f"Transcript with id {transcript_id} not found for summarization.")
        # No transcript_id to log against if not found, or log with null transcript_id
        return None

    if not db_transcript.original_text:
        print(f"Transcript with id {transcript_id} has no original text to summarize.")
        _log_to_commlog(db, transcript_id, "SUMMARY_SKIPPED", "Original text is missing.")
        return db_transcript
    
    prompt = f"Please summarize the following call transcript:\n\n---\n{db_transcript.original_text}\n---\n\nSummary:"

    try:
        print(f"Sending text to Gemini for transcript ID: {transcript_id}...")
        _log_to_commlog(db, transcript_id, "SUMMARY_GENERATION_STARTED", f"Prompt sent to Gemini model: {model.model_name}")
        
        response = await model.generate_content_async(prompt)
        generated_summary = response.text

        print(f"Summary received from Gemini for transcript ID: {transcript_id}")
        _log_to_commlog(db, transcript_id, "SUMMARY_GENERATION_SUCCESS", f"Summary received from Gemini.")

        db_transcript.summary_text = generated_summary
        db.add(db_transcript)
        db.commit()
        db.refresh(db_transcript)
        
        print(f"Transcript ID: {transcript_id} updated with summary.")
        return db_transcript
    
    except Exception as e:
        error_message = f"Error during Gemini API call or DB update for transcript {transcript_id}: {str(e)}"
        print(error_message)
        _log_to_commlog(db, transcript_id, "SUMMARY_GENERATION_FAILED", error_message)
        # db.rollback() # The session might be in an unrecoverable state here if the commit for summary_text failed.
                      # The background task's session management might need to be more robust.
        return None