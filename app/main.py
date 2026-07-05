from datetime import datetime, timezone

from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="Module 1 Task Tracker API",
    description="A minimal FastAPI REST API for a learning-project task tracker.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }