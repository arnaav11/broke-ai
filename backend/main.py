from fastapi import FastAPI
from routers import plaid_api

app = FastAPI(title="Inflation Tracker API")

# Include the Plaid routes
app.include_router(plaid_api.router, prefix="/api/plaid", tags=["Banking"])

@app.get("/")
def read_root():
    return {"status": "Backend is running"}