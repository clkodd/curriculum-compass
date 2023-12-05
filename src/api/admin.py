from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Resets the site.
    """
    with db.engine.begin() as connection:
        # Drop existing tables
        result = connection.execute(sqlalchemy.text(
            """
            TRUNCATE TABLE organizations
            RESTART IDENTITY
            CASCADE;

            TRUNCATE TABLE volunteers
            RESTART IDENTITY
            CASCADE
            """))
        
    if result != None:
        return "OK"
    else:
        raise Exception("Invalid removing of schedule")


@router.get("/organization_info/")
def get_organization_info():
    """ """
    sql = """
    SELECT o.name, o.org_id
    FROM organizations AS o
    """
    res = []
    with db.engine.begin() as connection:
        # Drop existing tables
        rows = connection.execute(sqlalchemy.text(
            sql))
    for row in rows:
        res.append({
            "organization_id": row.org_id,
            "organization": row.name
        })
    return res
