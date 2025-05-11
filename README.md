# CareIN AI - AI Call Summary Module

This project is a submission for the CareIN AI Technical Challenge. It's a full-stack application that accepts a call transcript via a backend API, summarizes it using the Gemini API, and stores/displays it in a frontend dashboard.

## Tech Stack

**Backend:**
*   FastAPI (Python)
*   PostgreSQL (Database)
*   SQLAlchemy (ORM)
*   Uvicorn (ASGI Server)
*   Google Generative AI (for Gemini API)
*   Python-dotenv (for environment variable management)

**Frontend:**
*   Next.js (React Framework)
*   TypeScript
*   Tailwind CSS (with PostCSS and Autoprefixer)
*   Mona Sans (Font)

**Database:**
*   PostgreSQL

## Project Structure

## Prerequisites

*   Python 3.9+ and Pip
*   Node.js 18+ and Npm (or Yarn)
*   A running PostgreSQL instance (if not using Docker for the database)
*   A Gemini API Key from Google AI Studio

## Environment Variables

Create the necessary `.env` files for the backend and frontend.

**1. Backend (`backend/.env`):**

```env
DATABASE_URL=postgresql://your_db_user:your_db_password@your_db_host:your_db_port/your_db_name
GEMINI_API_KEY=your_gemini_api_key
```
*   Replace placeholders with your actual PostgreSQL connection details and Gemini API Key.
*   If using the `docker-compose.yml` setup provided (which includes a Postgres service), the `DATABASE_URL` for the backend service will be: `postgresql://postgres:yoursecurepassword@db:5432/carein_db` (or whatever you set in `docker-compose.yml`).

**2. Frontend (`frontend/.env.local`):**

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```
*   This should point to where your backend API is running. If running backend via Docker with the provided `docker-compose.yml`, `http://localhost:8000/api/v1` is correct as Docker Compose will map the backend's port 8000 to the host's port 8000.

## Setup and Running the Application

### Option 1: Running Locally (Without Docker)

**1. Backend (FastAPI):**

   *   Navigate to the `backend` directory:
     ```
     cd backend
     ```
   *   Create a virtual environment (recommended):
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   *   Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   *   Ensure your PostgreSQL server is running and accessible.
   *   Update `backend/.env` with your `DATABASE_URL` and `GEMINI_API_KEY`.
   *   Run the FastAPI application:
     ```
     uvicorn app.main:app --reload
     ```
     The backend should be running on `http://localhost:8000`.

**2. Frontend (Next.js):**

   *   Navigate to the `frontend` directory (from the project root):
     ```
     cd ../frontend  # Or cd frontend if in project root
     ```
   *   Install dependencies:
     ```
     npm install
     ```
   *   Update `frontend/.env.local` if your backend is not on `http://localhost:8000/api/v1`.
   *   Run the Next.js development server:
     ```
     npm run dev
     ```
     The frontend should be running on `http://localhost:3000`.

### Option 2: Running with Docker Compose (Recommended for ease of use)

This method will build and run the backend, frontend, and a PostgreSQL database service.

**1. Prerequisites:**
   * Ensure Docker and Docker Compose are installed and running.

**2. Environment Variables:**
   * Create `backend/.env` in the `backend` directory with your `GEMINI_API_KEY`. The `DATABASE_URL` will be handled by Docker Compose, but you should use the one specified in the `docker-compose.yml` (e.g., `postgresql://postgres:yoursecurepassword@db:5432/carein_db`) if you were to connect from *within* the backend container. For the `.env` file, to make it easy for local development and Docker, you could set it to the Docker internal one or use separate configs. For simplicity with current setup:
        ```
        # backend/.env
        DATABASE_URL=postgresql://postgres:yoursecurepassword@db:5432/carein_db
        GEMINI_API_KEY=your_actual_gemini_api_key
        ```
   * Create `frontend/.env.local` in the `frontend` directory:
        ```
        # frontend/.env.local
        NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
        ```

**3. Build and Run:**
   * Navigate to the project root directory (`CareAI-Coding-Challenge`):
     ```
     cd /path/to/CareAI-Coding-Challenge
     ```
   * Build and start the services:
     ```
     docker-compose up --build
     ```
     *   Add `-d` to run in detached mode: `docker-compose up --build -d`
   * The frontend will be accessible at `http://localhost:3000`.
   * The backend API will be accessible at `http://localhost:8000`.
   * The API docs (Swagger UI) will be at `http://localhost:8000/docs`.

**4. To stop the services:**
   ```
   docker-compose down
   ```

## API Endpoints

The backend exposes the following main API endpoints (prefixed with `/api/v1`):

*   **Transcripts:**
    *   `POST /transcripts/`: Create a new transcript.
        *   Body: `{ "original_text": "string" }`
    *   `GET /transcripts/`: Get a list of transcripts.
    *   `GET /transcripts/{transcript_id}`: Get a specific transcript by ID.
    *   `POST /transcripts/{transcript_id}/rerun-summary`: Re-run summary for a transcript.
*   **CommLog:**
    *   `GET /commlogs/`: Get all communication logs.
    *   `GET /commlogs/transcript/{transcript_id}`: Get communication logs for a specific transcript.
*   **Admin:**
    *   `DELETE /admin/clear-tables`: Clears all data from `transcripts` and `commlogs` tables and resets ID sequences.

Refer to `http://localhost:8000/docs` (when the backend is running) for a detailed interactive API specification.

## Features

*   **Transcript Submission:** Accepts call transcripts via a backend API.
*   **AI Summarization:** Summarizes transcripts using the Gemini API.
*   **Database Storage:** Stores original transcripts, summaries, and communication logs in a PostgreSQL database.
*   **Frontend Dashboard:** Displays transcripts and their summaries.
*   **View CommLog:** Allows viewing communication logs for each transcript.
*   **Re-run Summary:** Button to trigger a re-summarization of a transcript, with a new entry in the commlog.
*   **Clear Database:** Admin endpoint to clear all tables for testing.

## Notes

*   The Gemini API requires a valid API key. Ensure this is set in `backend/.env`.
*   The application uses a dark theme with the Mona Sans font.
*   For development, the backend uses `uvicorn` with `--reload` and the Next.js frontend uses its hot-reloading development server.

---
