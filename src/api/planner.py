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

@router.post("/create")
def new_event(event_organizer_id: int):
    """ 
    Creates a new event.
    """
    return {"event_id": int}


@router.post("/{event_id}/{event_organizer_id}")
def get_event_plan(event_id: int, new_event: NewEvent):
    """ 
    Adds event traits to the specified event, using the event's ID.
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
                UPDATE event 
                SET name = :name, 
                    total_spots = :total_spots, 
                    min_age = :minimum_age, 
                    activity_level = :activity_level,
                    location = :location,
                    start_time = :start_time,
                    end_time = :end_time,
                    description = :description,
                WHERE event.event_id = :event_id
            """
        ), [{"name": new_event.name}, 
            {"total_spots": new_event.total_spots}, 
            {"minimum_age": new_event.minimum_age},
            {"location": new_event.location},
            {"start_time": new_event.start_time},
            {"end_time": new_event.end_time},
            {"description": new_event.description},
            {"event_id": event_id}
            ]).scalar()

    if result.rowcount == 1:
        return "OK"
    else:
        raise Exception("Invalid event_id")

#HAYLEY
@router.post("/{event_id}/{event_organizer_id}")
def delete_event(event_id):
    """ 
    Removes an event from a volunteer's schedule.
    """
    return "OK"


