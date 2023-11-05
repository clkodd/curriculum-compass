from fastapi  import APIRouter, Depends
from pydantic import BaseModel
from src.api  import auth
from src      import database as db
from datetime import datetime
import sqlalchemy


router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/", tags = "events")
def get_events():
    """ 
    Retreives the list of available events.
    """

    with db.engine.begin() as connection:
        events = connection.execute(sqlalchemy.text(
                """
                SELECT events.event_id, events.name, events.min_age, events.activity_level, 
                    events.location, events.start_time, events.end_time, events.description, 
                    (events.total_spots - COUNT(volunteer_schedule.event_id)) AS spots_left
                FROM events
                JOIN volunteer_schedule
                ON events.event_id = volunteer_schedule.event_id
                GROUP BY events.event_id
                ORDER BY start_time
                """
                ))

    event_list = []

    for row in events:
        if row.spots_left > 0:
            event_list.append(
                {
                    "event_id": row.event_id,
                    "name": row.name, 
                    "spots_left": row.spots_left,
                    "minimum_age": row.min_age,
                    "activity_level": row.activity_level,
                    "location": row.location,
                    "start_time": row.start_time,
                    "end_time": row.end_time,
                    "description": row.description,
                }
            )

    return event_list