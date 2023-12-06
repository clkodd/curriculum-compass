from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime, timedelta
from enum import Enum


router = APIRouter(
    prefix="/planner",
    tags=["planner"],
    dependencies=[Depends(auth.get_api_key)],
)

class activity_level_options(str, Enum):
    low = "low"
    low_med = "low_med"
    medium = "medium"
    med_high = "med_high"
    high = "high"
    extreme = "extreme"

class NewEvent(BaseModel):
    name: str
    total_spots: int
    minimum_age: int
    location: str
    start_time: datetime 
    end_time: datetime
    description: str


@router.post("/{event_organizer_id}/create")
def create_event(supervisor_id: int, new_event: NewEvent, activity_level: activity_level_options = activity_level_options.low):
    """ 
    Create event based on a supervisor_id.
    """
    activity_level_scale = {"low": 0, "low_med": 1, "medium": 2, "med_high": 3, "high": 4, "extreme": 5}
    target_datetime_utc = new_event.start_time.replace(tzinfo=None)

    # Get the current date and time in UTC
    current_datetime_utc = datetime.utcnow()

    if new_event.total_spots < 1:
        error_message = "Invalid event details; total_spots must be at least 1"
        raise HTTPException(status_code=400, detail=error_message)
    if new_event.minimum_age < 13 or new_event.minimum_age > 99:
        error_message = "Invalid event details; minimum age must be greater than 12 and less than 100"
        raise HTTPException(status_code=400, detail=error_message)
    if new_event.start_time > new_event.end_time:
        error_message = "Invalid event details; start_time is greater than end_time"
        raise HTTPException(status_code=400, detail=error_message)
    if (new_event.end_time - new_event.start_time).total_seconds() / 60 < 10:
        error_message = "Invalid event details; duration of event must be at least 10 minutes"
        raise HTTPException(status_code=400, detail=error_message)
    
    time_difference = target_datetime_utc - current_datetime_utc
    if time_difference < timedelta(days=1):
        error_message = "Invalid event details; start date must be after today " + str(current_datetime_utc)
        raise HTTPException(status_code=400, detail=error_message)
    
    activity_level_scaled = activity_level_scale[activity_level]


    with db.engine.begin() as connection:
        sup_info = connection.execute(sqlalchemy.text(
            """
            SELECT sup_name, email
            FROM supervisors
            WHERE sup_id = :sup_id
            """
        ), {"sup_id": supervisor_id}
            ).fetchone()
        
        print(sup_info)
        
        if sup_info == None:
            error_message = "Invalid supervisor"
            raise HTTPException(status_code=400, detail=error_message)

        find_duplicates = connection.execute(sqlalchemy.text(
            """
            SELECT name, location
            FROM events
            WHERE name = :name AND location = :location AND start_time = :start_time AND end_time = :end_time
            """
        ), [{"name": new_event.name, 
            "location": new_event.location,
            "start_time": new_event.start_time,
            "end_time": new_event.end_time
            }]).fetchone()
        
        if find_duplicates != None:
            error_message = "Invalid event; event already created " + find_duplicates.name
            raise HTTPException(status_code=400, detail=error_message)


        result = connection.execute(sqlalchemy.text(
            """
                INSERT INTO events (sup_id, name, total_spots, min_age, 
                                    activity_level, location, start_time, end_time, description)
                VALUES (:sup_id, :name, :total_spots, :min_age, 
                        :activity_level, :location, :start_time, :end_time, :description)
                RETURNING event_id
            """
        ), [{"sup_id": supervisor_id, 
            "name": new_event.name, 
            "total_spots": new_event.total_spots,
            "min_age": new_event.minimum_age,
            "activity_level": activity_level_scaled,
            "location": new_event.location,
            "start_time": new_event.start_time,
            "end_time": new_event.end_time,
            "description": new_event.description}
            ]).scalar()
        connection.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW event_summary;"))


    if result != None:
        return {"event_id": result, 
                "supervisor_name": sup_info.sup_name, 
                "supervisor_email": sup_info.email, 
                "event name": new_event.name, 
                "total_spots": new_event.total_spots,
                "min_age": new_event.minimum_age,
                "activity_level": activity_level,
                "location": new_event.location,
                "start_time": new_event.start_time,
                "end_time": new_event.end_time,
                "description": new_event.description
                }
    else:
        error_message = "Invalid event details; event not added"
        raise HTTPException(status_code=400, detail=error_message)


@router.delete("/{event_id}/")
def delete_event(event_id: int):
    """ 
    Deletes an event.
    """
    with db.engine.begin() as connection:

        result = connection.execute(sqlalchemy.text(
        """
        DELETE FROM events
        WHERE event_id = :event_id
        RETURNING event_id
        """
        ),{"event_id":event_id}).scalar()
        connection.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW event_summary;"))

    if result != None:
        return "Deleted event: " + str(event_id)
    else:
        error_message = "Invalid removing of event"
        raise HTTPException(status_code=400, detail=error_message)


