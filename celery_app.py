import os
from celery import Celery
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Initialize Celery and point it to our Docker Redis instance
app = Celery(
    "macro_pipeline",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
    include=["tasks"]  # Tells Celery to look for background jobs inside tasks.py
)

# Optional configuration settings
app.conf.timezone = "UTC"