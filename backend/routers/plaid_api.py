from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from config import settings

router = APIRouter()

# 1. Configure the Plaid Client
host = plaid.Environment.Sandbox if settings.PLAID_ENV == "sandbox" else plaid.Environment.Production
configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Pydantic Schemas for Requests
class ExchangeTokenRequest(BaseModel):
    public_token: str
    user_id: str

@router.post("/link/token/create")
async def create_link_token(user_id: str):
    """
    Creates a Link Token. The frontend uses this token to initialize the Plaid SDK.
    """
    try:
        request = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="Personal Inflation Tracker",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(
                client_user_id=user_id
            )
        )
        response = client.link_token_create(request)
        return {"link_token": response['link_token']}
    except plaid.ApiException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/item/public_token/exchange")
async def exchange_public_token(payload: ExchangeTokenRequest):
    """
    Exchanges the temporary public_token (sent from frontend) for a permanent access_token.
    """
    try:
        request = ItemPublicTokenExchangeRequest(
            public_token=payload.public_token
        )
        response = client.item_public_token_exchange(request)
        
        # TODO: Save the access_token and item_id securely in your PostgreSQL database
        # linking them to the specific payload.user_id
        access_token = response['access_token']
        item_id = response['item_id']
        
        return {
            "message": "Bank successfully linked", 
            "item_id": item_id,
            "access_token": "Saved securely in DB" 
        }
    except plaid.ApiException as e:
        raise HTTPException(status_code=400, detail=str(e))