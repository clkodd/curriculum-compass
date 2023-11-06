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

@router.post("/")
def new_volunteers(new_volunteer: NewVolunteer):
    """ """
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

    if volunteer_id != None:
        return {"volunteer_id": volunteer_id}
    else:
        raise Exception("Invalid creation of volunteer")

# ananya does 1.3 and 2.3
@router.post("/events/{event_id}")
# change - input volunteer id and event id. i want to add X event to a specific volunteer's schedule
def add_schedule_item(volunteer_id: int, event_id: int):
    """ """ 
    with db.engine.begin() as connection:
        event = connection.execute(sqlalchemy.text(
            """
            SELECT total_spots, min_age, start_time, end_time
            FROM events
            """))
    r1 = event.first()
    cur_spots = r1.total_spots
    min_age = r1.min_age
    start_time = r1.start_time
    end_time = r1.end_time
    # need to add a check for timing, how?
    # TODO: DON'T ADD SAME EVENT TWICE

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
                """),
                [{"volunteer_id": volunteer_id, "event_id": event_id}])
    print("EVENT ADDED: ", event_id, " VOLUNTEER: ", volunteer_id)       
    return "OK"

# need to descrease number of spots in events table
# ANANYA
@router.post("/{volunteer_id}/register")
def total_registered_events(volunteer_id: int): # total_registered_event title changed
    """ """
    # TODO: what happens if they aren't registered for any events?

    total_events_registered = 0
    total_hours = 0
    with db.engine.begin() as connection:   
        result = connection.execute(sqlalchemy.text(
                """
                SELECT DATE_PART('hour', SUM(end_time - start_time)) AS total_hours, COUNT(events.event_id) AS total_events
                FROM events
                JOIN volunteer_schedule ON volunteer_schedule.event_id = events.event_id 
                WHERE volunteer_id = :volunteer_id
                """), 
                [{"volunteer_id": volunteer_id}])
        first_row = result.first()
        total_hours = first_row.total_hours
        total_events_registered = first_row.total_events
    return {"total_events_registered": total_events_registered, "total_hours": total_hours}

@router.post("/{volunteer_id}/remove")
def remove_schedule_item(volunteer_id: int, event_id: int):
    """ """
    # TODO: only return "OK" if sucessfully deleted otherwise raise Exception

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
            DELETE FROM volunteer_schedule
            WHERE volunteer_schedule.event_id = event_id AND volunteer_schedule.volunteer_id = volunteer_id
            """),
            [{"event_id": event_id, "volunteer_id": volunteer_id}])
    return "OK"
