from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewOrganization(BaseModel):
    name: str
    city: str
    verified: bool

@router.post("/")
def new_organizations(new_organization: NewOrganization):
    """ """
    with db.engine.begin() as connection:
        org_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO organizations (name, city, verified)
                VALUES (:name, :city, :verified)
                RETURNING org_id
            """
        ), [{"name": new_organization.name, 
             "city": new_organization.city, 
             "verified": new_organization.verified}]).scalar()

    if org_id != None:
        return {"org_id": org_id}
    else:
        raise Exception("Invalid creation of organizer")

class NewSupervisor(BaseModel):
    sup_name: str
    email: str

@router.post("/{org_id}/supervisor")
def new_supervisors(org_id: int, new_supervisor: NewSupervisor):
    """ """
    with db.engine.begin() as connection:
        sup_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO supervisors (sup_name, org_id, email)
                VALUES (:sup_name, :org_id, :email)
                RETURNING sup_id
            """
        ), [{"sup_name": new_supervisor.sup_name, 
            "org_id": org_id, 
            "email": new_supervisor.email}]).scalar()

    if sup_id != None:
        return {"sup_id": sup_id}
    else:
        raise Exception("Invalid creation of supervisor")
