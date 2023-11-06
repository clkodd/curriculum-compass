from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

#fyi renamed it planner bc there were naming issues when it was event-planner bc of the -
#change in api spec
router = APIRouter(
    prefix="/planner",
    tags=["planner"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewEvent(BaseModel):
    name: str
    total_spots: int
    minimum_age: int
    activity_level: int
    location: str
    start_time: str #change these to strings bc i don't think datetime is a datatype but feel free to edit this
    end_time: str
    description: str


@router.post("/{event_organizer_id}/create")
def create_event(event_organizer_id: int, new_event: NewEvent):
    """ 
    Adds event traits to the specified event, using the event's ID.
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                INSERT INTO events (sup_id, name, total_spots, min_age, 
                                    activity_level, location, start_time, end_time, description)
                VALUES (:sup_id, :name, :total_spots, :min_age, 
                        :activity_level, :location, :start_time, :end_time, :description)
                RETURNING event_id
            """
        ), [{"sup_id": event_organizer_id, 
             "name": new_event.name, 
             "total_spots": new_event.total_spots,
             "min_age": new_event.minimum_age,
             "activity_level": new_event.activity_level,
             "location": new_event.location,
             "start_time": new_event.start_time,
             "end_time": new_event.end_time,
             "description": new_event.description}
            ]).scalar()

    if result != None:
        return {"event_id": result}
    else:
        raise Exception("Invalid event details; event not added")

#HAYLEY
@router.post("/{event_id}/{event_organizer_id}")
def delete_event(event_id):
    """ 
    Removes an event from a volunteer's schedule.
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
        """
        DELETE FROM events
        WHERE event_id = :event_id
        """
        ),{"event_id":event_id})
    return "OK"


