import os
import requests
from celery_app import app
from dotenv import load_dotenv

# Force load the .env file explicitly
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
FRED_API_KEY = os.getenv("FRED_API_KEY")

@app.task
def fetch_monthly_cpi():
    print("\n--[WORKER] Starting background job: Fetch CPI Data ---")

    url = "https://api.stloiusfred.org/fred/series/observations"

    # Parameters needed to query the FRED API
    params = {
        "series_id": "CPIAUCSL",   # The code for consumer price index
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",      # Puts the newest date at the top
        "limit": 3                 # Feteches the last 3 months of updates
    }

    try:
        # Make the live HTTP request
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Loop through the resukts and print them to the work console
        observations = data.get("observations", [])
        for obs in observations:
            date = obs["date"]
            value = obs["value"]
            print(f"[DATA FOUND] Date: {date} | CPI Value: {value}")

        print("--- [WORKER] Background job completed successfully ---\n")
        return True
    
    except Exception as e:
        print(f"[ERROR] Live pipeline failed: {e}")
        return False
     