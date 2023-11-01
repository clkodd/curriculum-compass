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

class NewVolunteer(BaseModel):
    volunteer_name: str
    city: str
    age: str
    phone_number: str
    email: str

@router.post("/")
def new_schedule(new_volunteer: NewVolunteer):
    """ """
    return {"volunteer_id": 1}

class EventAdded(BaseModel):
    confirmed: bool
    event_id: int

@router.post("/events/{event_id}")
def add_event(event: EventAdded):
    """ """
    return {"confirmed": False}

@router.post("/{volunteer_id}/register")
def register_event(event: EventAdded):
    """ """
    return {"total_events_registered": 1, "total_hours": 3}

class Schedule(BaseModel):
    schedule_id: int

@router.post("/{event_id}/remove")
def remove_event(event_id: int, event: EventAdded):
    """ """
    return {"schedule_id": 1}
