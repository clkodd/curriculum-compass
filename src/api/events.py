from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime

router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewEvent(BaseModel):
    event_id: int
    name: str
    spots_left: int
    minimum_age: int
    activity_level: int
    location: str
    start_time: datetime 
    end_time: datetime
    description: str

@router.get("/")
def get_events(new_event: NewEvent):
    """ 
    Retreives the list of available events.
    """
    return [
        {
             "event_id": 1,
            "name": "volunteer event lol", 
            "spots_left": 5,
            "minimum_age": 16,
            "activity_level": 2,
            "location": "San Luis Obispo",
            "start_time": datetime,
            "end_time": datetime,
            "description": "description tbd lol"
        }
    ]