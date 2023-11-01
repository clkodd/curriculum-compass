from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

#fyi renamed it planner bc there were naming issues when it was event-planner bc of the -
#change in api spec
router = APIRouter(
    prefix="/planner",
    tags=["planner"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewEvent(BaseModel):
    name: str
    spots_left: int
    minimum_age: int
    activity_level: int
    location: str
    start_time: str #change these to strings bc i don't think datetime is a datatype but feel free to edit this
    end_time: str
    description: str

@router.post("/create")
def new_event():
    """ 
    Creates a new event.
    """
    return {"event_id": int}


@router.post("/{event_id}/{event_organizer_id}")
def get_event_plan(new_event: NewEvent):
    """ 
    Adds event traits to the specified event, using the event's ID.
    """
    return "OK"

@router.post("/{event_id}/{event_organizer_id}")
def delete_event(event_id):
    """ 
    Removes an event from a volunteer's schedule.
    """
    return "OK"


