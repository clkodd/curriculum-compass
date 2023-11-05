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

@router.get("/")
def get_events():
    """ 
    Retreives the list of available events.
    """
    return [
        {
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