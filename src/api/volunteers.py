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
    email: str

@router.post("/volunteers")
def new_volunteer(new_volunteer: NewVolunteer):
    """ """
    with db.engine.begin() as connection:
        volunteer_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO volunteers (name, city, age, email)
                VALUES (:volunteer_name, :city, :age, :email)
                RETURNING volunteer_id
            """
        ), [{"volunteer_name": new_volunteer.volunteer_name}, 
            {"city": new_volunteer.city}, 
            {"age": new_volunteer.age},
            {"email": new_volunteer.email}]).scalar()


    return {"volunteer_id": volunteer_id}

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
