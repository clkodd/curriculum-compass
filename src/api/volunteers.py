from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from datetime import datetime
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
def new_volunteers(new_volunteer: NewVolunteer):
    """ """
    #maybe create a schedule_id here as well that can be passed into the next function?
    with db.engine.begin() as connection:
        volunteer_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO volunteers (name, city, age, email)
                VALUES (:volunteer_name, :city, :age, :email)
                RETURNING volunteer_id
            """
        ), [{"volunteer_name": new_volunteer.volunteer_name, 
             "city": new_volunteer.city, 
            "age": new_volunteer.age,
            "email": new_volunteer.email}]).scalar()


    return {"volunteer_id": volunteer_id}

# ananya does 1.3 and 2.3
@router.post("/events/{event_id}")
# change - input volunteer id and event id. i want to add X event to a specific volunteer's schedule
def add_event(volunteer_id: int, event_id: int):
    """ """
    
    with db.engine.begin() as connection:
        event = connection.execute(sqlalchemy.text(
            """
            SELECT total_spots, min_age, timeslot
            FROM events
            """))
    r1 = event.first()
    cur_spots = r1.total_spots
    min_age = r1.min_age
    # need to add a check for timing, how?

    with db.engine.begin() as connection:
        volunteer = connection.execute(sqlalchemy.text(
            """
            SELECT age
            FROM volunteers
            """))
    r2 = volunteer.first()
    age = r2.age

    if cur_spots >= 1 and age >= min_age:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                """
                INSERT INTO volunteer_schedule
                (volunteer_id, event_id) 
                SELECT :volunteer_id, :event_id 
                FROM events WHERE events.event_id = :event_id
                RETURNING schedule_id
                """),
                [{"volunteer_id": volunteer_id, "event_id": event_id}])
            schedule_id = result.scalar()
    print("EVENT ADDED: ", event_id, " VOLUNTEER: ", volunteer_id)       
    return {"schedule_id": schedule_id}

# need to descrease number of spots in events table
@router.post("/{volunteer_id}/register")
def register_event(event_id: int):
    """ """
    return {"total_events_registered": 1, "total_hours": 3}

class Schedule(BaseModel):
    schedule_id: int

#pretty sure we need to input volunteer_id as well, what do yall think?
@router.post("/{event_id}/remove")
def remove_event(volunteer_id: int, event_id: int):
    """ """
    #need to update events table back to add a spot
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
            DELETE FROM volunteer_schedule
            WHERE volunteer_schedule.event_id = event_id AND volunteer_schedule.volunteer_id = volunteer_id
            """),
            [{"event_id": event_id, "volunteer_id": volunteer_id}])
    return "OK"
