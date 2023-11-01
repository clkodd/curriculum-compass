from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

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
    start_time: str #change these to strings bc i don't think datetime is a datatype but feel free to edit this
    end_time: str
    description: str

@router.post("/")
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
            "start_time": "2:00pm",
            "end_time": "5:00pm",
            "description": "description tbd lol"
        }
    ]