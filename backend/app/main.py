from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="InPulse Academic Intelligence API",
    description="Read-only Analytics API for InPulse Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],  # Only GET and OPTIONS for read-only
    allow_headers=["*"],
)

app.include_router(analytics.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FastAPI is running"}
