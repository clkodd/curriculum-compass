from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from src.api import auth, planner
import sqlalchemy
from datetime import date, datetime
from src import database as db
from typing import List

router = APIRouter(
    prefix="/volunteers",
    tags=["volunteers"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewVolunteer(BaseModel):
    volunteer_name: str
    city: str
    email: EmailStr
    birthday: date

@router.post("/")
def new_volunteers(new_volunteer: NewVolunteer):
    """Create a new volunteer."""

    # Validate the email format
    email = new_volunteer.email

    #validate age
    today = date.today()
    age = today.year - new_volunteer.birthday.year - ((today.month, today.day) < (new_volunteer.birthday.month, new_volunteer.birthday.day))
    
    min_age = 13
    max_age = 99

    if not (min_age <= age <= max_age):
        error_message = "Invalid Age"
        raise HTTPException(status_code=400, detail=error_message)

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            INSERT INTO volunteers (name, city, birthday, email)
            VALUES (:volunteer_name, :city, :birthday, :email)
            ON CONFLICT (email) DO NOTHING
            RETURNING volunteer_id
            """
        ), {
            "volunteer_name": new_volunteer.volunteer_name,
            "city": new_volunteer.city,
            "birthday": new_volunteer.birthday,
            "email": email
        })
        volunteer_id = result.scalar()

    if volunteer_id is not None:
        return {"volunteer_id": volunteer_id}
    else:
        error_message = "User with this email already exists"
        raise HTTPException(status_code=400, detail=error_message)


@router.post("/{volunteer_id}/update")
def update_volunteer_info(volunteer_id: int, 
        volunteer_name: str="",
        city: str="",
        email: EmailStr=None,
        birthday:date=None):
    set_clause = {}

    if volunteer_name:
        set_clause["name"] = volunteer_name
    if city:
        set_clause["city"] = city
    if email:
        set_clause["email"] = email
    if birthday:
        set_clause["birthday"] = birthday

    if not set_clause:
        error_message = "No information to edit volunteer"
        raise HTTPException(status_code=400, detail=error_message)

    set_clause_sql = ", ".join([f"{key} = :{key}" for key in set_clause.keys()])

    """Update volunteer information."""
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            f"""
            UPDATE volunteers
            SET {set_clause_sql}
            WHERE volunteer_id = :volunteer_id
            """
        ), {"volunteer_id": volunteer_id, **set_clause})

    return "OK"


@router.post("/events/{event_id}")
def add_schedule_item(volunteer_id: int, event_id: int):
    """ """

    with db.engine.begin() as connection:
        volunteer = connection.execute(sqlalchemy.text(
            """
            SELECT volunteer_id, date_part('year', current_date) - date_part('year', birthday) AS age
            FROM volunteers
            WHERE volunteer_id = :volunteer_id
            """),
            {"volunteer_id": volunteer_id})
        first_row = volunteer.first()

        if first_row is None:
            error_message = "Volunteer Doesn't Exist"
            raise HTTPException(status_code=400, detail=error_message)

        age = first_row.age

        existing_event = connection.execute(sqlalchemy.text(
            """
            SELECT volunteer_id
            FROM volunteer_schedule
            WHERE volunteer_id = :volunteer_id AND event_id = :event_id
            """),
            {"volunteer_id": volunteer_id, "event_id": event_id})

        if existing_event.first():
            error_message = "Event already in volunteer's schedule."
            raise HTTPException(status_code=400, detail=error_message)
   
        event = connection.execute(sqlalchemy.text(
            """
            SELECT event_id, min_age, total_spots, start_time, end_time
            FROM events
            WHERE event_id = :event_id
            """),
            {"event_id": event_id})
        event_details = event.first()

        if event_details is None:
            error_message = "Event Doesn't Exist"
            raise HTTPException(status_code=400, detail=error_message)

        min_age = event_details.min_age
        tot_spots = event_details.total_spots

        if age < min_age:
            error_message = "Not old enough to sign up for this event"
            raise HTTPException(status_code=400, detail=error_message)

        if event_details:
            event_start_time = event_details.start_time
            event_end_time = event_details.end_time

        spots_filled = connection.execute(sqlalchemy.text(
            """
            SELECT COUNT(*) AS spots
            FROM volunteer_schedule
            WHERE event_id = :event_id
            """
        ),
            {"event_id": event_id})
        first_row = spots_filled.first()
        spots = first_row.spots  
        print(spots)
        print(tot_spots)
        if spots >= tot_spots:
            error_message = "The spots for this event are already full"
            raise HTTPException(status_code=400, detail=error_message)

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
            error_message = "Timing conflict"
            raise HTTPException(status_code=400, detail=error_message)

        connection.execute(sqlalchemy.text(
            """
            INSERT INTO volunteer_schedule (volunteer_id, event_id) 
            VALUES (:volunteer_id, :event_id)
            """),
            {"volunteer_id": volunteer_id, "event_id": event_id})
        connection.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW event_summary;"))
    print("EVENT ADDED: ", event_id, " VOLUNTEER: ", volunteer_id)   
    return "OK"


@router.post("/{volunteer_id}/display_registered_events")
def display_registered_events(volunteer_id: int):
    """ """
    total_events_registered = 0
    total_hours = 0
    with db.engine.begin() as connection:   
        result = connection.execute(sqlalchemy.text(
                """
                SELECT COALESCE(DATE_PART('hour', SUM(end_time - start_time)), 0) AS total_hours, COUNT(events.event_id) AS total_events
                FROM events
                JOIN volunteer_schedule ON volunteer_schedule.event_id = events.event_id 
                WHERE volunteer_id = :volunteer_id
                """), 
                [{"volunteer_id": volunteer_id}])
        first_row = result.first()
        total_hours = first_row.total_hours
        total_events_registered = first_row.total_events
    return {"total_events_registered": total_events_registered, "total_hours": total_hours}

@router.delete("/{volunteer_id}/remove")
def remove_schedule_item(volunteer_id: int, event_id: int):
    """ """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            DELETE FROM volunteer_schedule
            WHERE volunteer_schedule.event_id = :event_id AND volunteer_schedule.volunteer_id = :volunteer_id
            RETURNING schedule_id
            """),
            [{"event_id": event_id, "volunteer_id": volunteer_id}]).scalar()
        
        print(result)
        if result is None:
            raise HTTPException(status_code=404, detail="Can't delete event")
    return "OK"

@router.get("/{volunteer_id}/events")
def get_volunteer_events(volunteer_id: int):
    """Get the events for a volunteer."""
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT name, total_spots, location, activity_level, start_time, end_time, description
            FROM events
            JOIN volunteer_schedule ON volunteer_schedule.event_id = events.event_id
            WHERE volunteer_schedule.volunteer_id = :volunteer_id
            """
        ), {"volunteer_id": volunteer_id})

        volunteer_events = result.fetchall()

    if not volunteer_events:
        raise HTTPException(status_code=404, detail="No events found for the volunteer")

    schedule = []
    for ve in volunteer_events:
        schedule.append(
            {
                "name": ve.name,
                "total spots": ve.total_spots,
                "location": ve.location, 
                "activity_level": ve.activity_level,
                "start_time": ve.start_time,
                "end_time": ve.end_time,
                "description": ve.description,
            })
    return schedule
