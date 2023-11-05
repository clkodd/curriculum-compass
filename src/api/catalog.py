from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/volunteers",
    tags=["volunteers"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/events")
def get_events():
    """ """
    return [
        {
        "event_id": 1,
        "name": "Bob", 
        "spots_left": 2,
        "minimum_age": 20,
        "activity_level": 2,
        "location": "LA", 
        "start_time": "10 am",
        "end_time": "11 am",
        "description": "get groceries"
        }
    ]