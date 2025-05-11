import google.generativeai as genai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.transcript import Transcript
from app.schemas.transcript import TranscriptUpdate

try:
    genai.configure(api_key = settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini: {e}. Summarization might not work as expected!")

try:
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
except Exception as e:
    print(f"Error initializing Gemini Model: {e}. Summarization might not work as expected!")
    model = None

async def generate_summary_for_transcript(db: Session, transcript_id: int) -> Transcript | None:
    """
    Fetch a transcript, generate summary using Gemini API
    Return updated transcript if obtained successfully, else return None
    """
    if not model:
        print("Gemini model not initialized! Skipping summarization!")
        return None
    
    db_transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not db_transcript:
        print(f"Transcript with id {transcript_id} not found!")

    if not db_transcript.original_text:
        print(f"Transcript with id {transcript_id} has no original text to summarize.")
        return db_transcript
    
    prompt = f"Please summarize the following call transcript:\n\n---\n{db_transcript.original_text}\n---\n\nSummary:"

    try:
        print(f"Sending text to Gemini for transcript ID: {transcript_id}...")
        response = await model.generate_content_async(prompt)

        generated_summary = response.text
        print(f"Summary received from Gemini for transcript ID: {transcript_id}")

        db_transcript.summary_text = generated_summary
        db.add(db_transcript)
        db.commit()
        db.refresh(db_transcript)
        
        print(f"Transcript ID: {transcript_id} updated with summary.")
        return db_transcript
    
    except Exception as e:
        print(f"Error during Gemini API call or DB update for transcript {transcript_id}: {e}")
        return None