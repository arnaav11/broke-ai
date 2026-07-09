JWT_ALGORITHM = "HS256"

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
    PLAID_SECRET = os.getenv("PLAID_SECRET")
    PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

settings = Settings()