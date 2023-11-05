from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """
    with db.engine.begin() as connection:
        # Drop existing tables
        connection.execute(sqlalchemy.text(
            "TRUNCATE events, organizations, supervisors, volunteer_schedule, volunteers CASCADE"))
        
    return "OK"


@router.get("/organization_info/")
def get_organization_info():
    """ """
    sql = """
    SELECT o.name
    FROM organizations AS o
    WHERE o.verified = TRUE
    """
    res = []
    with db.engine.begin() as connection:
        # Drop existing tables
        rows = connection.execute(sqlalchemy.text(
            sql))
    for row in rows:
        res.append({
            "organization": row.name
        })
    return {
        "shop_name": "Potion Shop",
        "shop_owner": "Potion Seller",
    }
