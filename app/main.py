import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router, AuthMiddleware

load_dotenv(find_dotenv())

log_directory = str(os.getenv("LOGS_PATH"))
os.makedirs(log_directory, exist_ok=True)

app = FastAPI()

today = datetime.now().isoformat()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

app.include_router(api_router, prefix="/api")


@app.get("/")
def get_root():
    return {
        "description": "API endpoints for v1 services",
        "deployment": today,
        "version": "v1.0.0",
        "environment": "development",
    }
