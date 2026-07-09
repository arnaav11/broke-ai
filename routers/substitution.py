from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from databases.database import get_db
from databases.models import LocationNode

router = APIRouter()

@router.get("/suggest_substitutes")
def get_substitutes(user_lon: float, user_lat: float, target_category: str, max_price: float, db: Session = Depends(get_db)):
    search_radius_meters = 1000 
    
    # Create a spatial point using Well-Known Text (WKT)
    # Important: PostGIS expects POINT(Longitude Latitude)
    user_point = WKTElement(f'POINT({user_lon} {user_lat})', srid=4326)
    
    # Execute the spatial query
    substitutes = db.query(LocationNode).filter(
        LocationNode.category == target_category,
        LocationNode.price_level <= max_price,
        func.ST_DWithin(LocationNode.location, user_point, search_radius_meters)
    ).all()
    
    return {"alternatives": substitutes}