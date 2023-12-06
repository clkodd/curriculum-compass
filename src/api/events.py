from fastapi  import APIRouter, Depends
from pydantic import BaseModel
from src.api  import auth
from src      import database as db
from datetime import date
import sqlalchemy
from enum import Enum


router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[Depends(auth.get_api_key)],
)

class search_sort_options(str, Enum):
    event_id = "event_id"
    start_date = "start_date"
    organization = "organization"
    min_age = "min_age"
    spots_left = "available_spots"
    activity_level = "activity_level"
    location = "location"
    supervisor_email = "supervisor_email"
    event_name = "event_name"
    
class activity_level_options(str, Enum):
    low = "low"
    low_med = "low_med"
    medium = "medium"
    med_high = "med_high"
    high = "high"
    extreme = "extreme"



class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"


@router.get("/")
def search(
        event_id: int = None,
        start_date: date = None,
        organization: str = "",
        min_age: int = 13,
        spots_left: int = 1,
        activity_level: activity_level_options = activity_level_options.low,
        location: str = "",
        event_name: str = "",
        supervisor_email: str = "",
        sort_col: search_sort_options = search_sort_options.start_date,
        sort_order: search_sort_order = search_sort_order.desc
    ):
    """ 
    Retrieves the list of available events.
    
    Activity level insert gives activities that can be done with insert activity or easier
    Min_age gives values that allow for that minimum age and older
    Spots_left returns values that have n spots left or more
    """

    with db.engine.begin() as connection:
        sql = f"""
            SELECT
            event_id,
            name,
            spots_left,
            min_age,
            activity_level,
            location,
            start_time,
            end_time,
            description,
            sup_id,
            org_name,
            sup_email
            FROM event_summary
            WHERE start_time > now() AND spots_left >= :spots_left
        """

        inp = {"spots_left": spots_left}
        if event_id:
            sql += " AND event_id = :event_id"
            inp["event_id"] = event_id
        if start_date:
            sql += " AND start_time::text ILIKE :start_date"
            inp["start_date"] = f"{start_date}%"

        if organization:
            sql += " AND org_name ILIKE :organization"
            inp["organization"] = f"%{organization}%"

        if min_age:
            sql += " AND min_age >= :min_age"
            inp["min_age"] = min_age

        if activity_level:
            activity_level_mapping = {
                activity_level_options.low: 0,
                activity_level_options.low_med: 1,
                activity_level_options.medium: 2,
                activity_level_options.med_high:3,
                activity_level_options.high: 4,
                activity_level_options.extreme: 5,
            }
            sql += f" AND activity_level >= {activity_level_mapping[activity_level]}"

        if location:
            sql += " AND location ILIKE :location"
            inp["location"] = f"%{location}%"

        if event_name:
            sql += "  AND name ILIKE :event_name"
            inp["event_name"] = f"%{event_name}%"

        if supervisor_email:
            sql += " AND sup_email ILIKE :supervisor_email"
            inp["supervisor_email"] = f"%{supervisor_email}%"

        sort_col_mapping = {
            search_sort_options.start_date: "start_time",
            search_sort_options.organization: "org_name",
            search_sort_options.min_age: "min_age",
            search_sort_options.spots_left: "spots_left",
            search_sort_options.activity_level: "activity_level",
            search_sort_options.location: "location",
        }

        sql += f" ORDER BY {sort_col_mapping[sort_col]} {sort_order.value}"

        events = connection.execute(sqlalchemy.text(sql), inp).all()

                

    event_list = []

    for row in events:
        event_list.append(
            {
                "event_id": row.event_id,
                "organization_name": row.org_name,
                "name": row.name, 
                "supervisor_email": row.sup_email,
                "spots_left": row.spots_left,
                "minimum_age": row.min_age,
                "activity_level": row.activity_level,
                "location": row.location,
                "start_date": row.start_time,
                "end_time": row.end_time,
                "description": row.description,
            }
        )
    if event_list:
        return event_list
    return {"message": "No events available at the moment."}