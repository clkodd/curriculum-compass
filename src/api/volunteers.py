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
    age: int
    email: str

@router.post("/")
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

    if volunteer_id != None:
        return {"volunteer_id": volunteer_id}
    else:
        raise Exception("Invalid creation of volunteer")

@router.post("/events/{event_id}")
def add_schedule_item(volunteer_id: int, event_id: int):
    """ """

    with db.engine.begin() as connection:
        volunteer = connection.execute(sqlalchemy.text(
            """
            SELECT age
            FROM volunteers
            """))
    r2 = volunteer.first()
    age = r2.age

    with db.engine.begin() as connection:
        existing_event = connection.execute(sqlalchemy.text(
            """
            SELECT volunteer_id
            FROM volunteer_schedule
            WHERE volunteer_id = :volunteer_id AND event_id = :event_id
            """),
            {"volunteer_id": volunteer_id, "event_id": event_id})

        if existing_event.first():
            return "Event already in volunteer's schedule."

    with db.engine.begin() as connection:
        event = connection.execute(sqlalchemy.text(
            """
            SELECT total_spots, min_age, start_time, end_time
            FROM events
            """))
    event_details = event.first()
    cur_spots = event_details.total_spots
    min_age = event_details.min_age
    start_time = event_details.start_time
    end_time = event_details.end_time
    

    if event_details:
        event_start_time = event_details.start_time
        event_end_time = event_details.end_time

        with db.engine.begin() as connection:
            conflicts = connection.execute(sqlalchemy.text(
                """
                SELECT vs.volunteer_id
                FROM volunteer_schedule vs
                JOIN events e ON vs.event_id = e.event_id
                WHERE vs.volunteer_id = :volunteer_id
                AND (
                    (e.start_time >= :event_start_time AND e.start_time < :event_end_time)
                    OR (e.end_time > :event_start_time AND e.end_time <= :event_end_time)
                )
                """),
                {"volunteer_id": volunteer_id, "event_start_time": event_start_time, "event_end_time": event_end_time})

            if conflicts.first():
                    return "Timing conflict"

    if cur_spots >= 1 and age >= min_age:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                """
                INSERT INTO volunteer_schedule (volunteer_id, event_id) 
                VALUES (:volunteer_id, :event_id)
                """),
                {"volunteer_id": volunteer_id, "event_id": event_id})
    print("EVENT ADDED: ", event_id, " VOLUNTEER: ", volunteer_id)   
    return "OK"

# need to descrease number of spots in events table
# ANANYA
@router.post("/{volunteer_id}/register")
def register_event(volunteer_id: int):
    """ """
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
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            DELETE FROM volunteer_schedule
            WHERE volunteer_schedule.event_id = :event_id AND volunteer_schedule.volunteer_id = :volunteer_id
            """),
            [{"event_id": event_id, "volunteer_id": volunteer_id}])
    if result != None:
        return "OK"
    else:
        raise Exception("Invalid removing of schedule")
