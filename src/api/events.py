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

    #how does total_spots work confusion? should we just change it to spots left?
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("""
        SELECT name, total_spots, min_age, activity_level, location, start_time, end_time, description
        FROM events
        """))
        available_events = []
        for row in result:
            available_events.append(
                {
                "name": row.name, 
                "spots_left": row.total_spots,
                "minimum_age": row.min_age,
                "activity_level": row.activity_level,
                "location": row.location,
                "start_time": row.start_time,
                "end_time": row.end_time,
                "description": row.description,
            }
            )
    print(f"available_events:", available_events)
    return available_events