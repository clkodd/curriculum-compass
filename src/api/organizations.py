from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/volunteers",
    tags=["volunteers"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewOrganization(BaseModel):
    name: str
    city: str
    verified: bool

@router.post("/organization")
def new_organizations(new_organization: NewOrganization):
    """ """
    with db.engine.begin() as connection:
        org_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO organizations (name, city, verified)
                VALUES (:name, :city, :verified)
                RETURNING org_id
            """
        ), [{"name": new_organization.name}, 
            {"city": new_organization.city}, 
            {"verified": new_organization.verified}]).scalar()


    return {"org_id": org_id}

class NewSupervisor(BaseModel):
    sup_name: str
    email: str

@router.post("/organization/{org_id}/supervisor")
def new_supervisors(org_id: int, new_supervisor: NewSupervisor):
    """ """
    with db.engine.begin() as connection:
        sup_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO supervisors (name, org_id, email)
                VALUES (:name, :org_id, :email)
                RETURNING sup_id
            """
        ), [{"name": new_supervisor.name}, 
            {"org_id": org_id}, 
            {"email": new_supervisor.email}]).scalar()


    return {"sup_id": sup_id}