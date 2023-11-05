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
    print(new_organization.name)
    print(new_organization.city)
    print(new_organization.verified)
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


    return {"org_id": org_id}

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


    return {"sup_id": sup_id}