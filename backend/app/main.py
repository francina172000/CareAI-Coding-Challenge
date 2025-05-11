from fastapi import FastAPI
from app.core.config import settings
from app.core.db import Base, engine

from app.models import transcript as transcript_model

from app.api.v1.api import api_router as api_v1_router

def create_db_and_tables():
    print("Attempting to create database tables if they do not exist...")
    try:
        Base.metadata.create_all(bind = engine, checkfirst = True)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

create_db_and_tables()

app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url = f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_v1_router, prefix = settings.API_V1_STR)

@app.get("/", tags = ['Root'])
async def read_root():
    return {"message": "Welcome to the Call Summary API!"}