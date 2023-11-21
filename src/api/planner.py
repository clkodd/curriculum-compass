from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from datetime import datetime
from enum import Enum


router = APIRouter(
    prefix="/planner",
    tags=["planner"],
    dependencies=[Depends(auth.get_api_key)],
)

class activity_level_options(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

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
    activity_level_scale = {"low": 1, "medium": 2, "high": 3}

    if new_event.total_spots < 1:
        error_message = "Invalid event details; total_spots must be at least 1"
        raise HTTPException(status_code=400, detail=error_message)
    if new_event.minimum_age < 5 or new_event.minimum_age > 90:
        error_message = "Invalid event details; minimum age must be greater than 5 and less than 90"
        raise HTTPException(status_code=400, detail=error_message)
    if new_event.start_time > new_event.end_time:
        error_message = "Invalid event details; start_time is greater than end_time"
        raise HTTPException(status_code=400, detail=error_message)
    elif (new_event.end_time - new_event.start_time).total_seconds() / 60 < 10:
        error_message = "Invalid event details; duration of event must be at least 10 minutes"
        raise HTTPException(status_code=400, detail=error_message)
    
    activity_level_scaled = activity_level_scale[activity_level]


    with db.engine.begin() as connection:
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
        
        sup_info = connection.execute(sqlalchemy.text(
            """
            SELECT sup_name, email
            FROM supervisors
            WHERE sup_id = :sup_id
            """
        ), {"sup_id": supervisor_id}
            ).fetchone()

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


@router.post("/{event_id}/")
def delete_event(event_id: int):
    """ 
    Deletes an event.
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
        """
        DELETE FROM events
        WHERE event_id = :event_id
        """
        ),{"event_id":event_id})
    if result != None:
        return "Deleted event: " + str(event_id)
    else:
        error_message = "Invalid removing of event"
        raise HTTPException(status_code=400, detail=error_message)


