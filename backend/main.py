from fastapi import FastAPI
from routers import plaid_api, substitution

app = FastAPI(title="Inflation Tracker API")

app.include_router(plaid_api.router, prefix="/api/plaid", tags=["Banking"])
app.include_router(substitution.router, prefix="/api/engine", tags=["Substitution"])

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

#this file is useless i think