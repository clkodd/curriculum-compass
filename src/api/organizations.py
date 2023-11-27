from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/")
def new_organizations(new_organization: NewOrganization):
    """ """
    with db.engine.begin() as connection:
        find_duplicates = connection.execute(sqlalchemy.text(
            """
            SELECT name
            FROM organizations
            WHERE name = :name
            """
        ), [{"name": new_organization.name
            }]).fetchone()
        
        if find_duplicates != None:
            error_message = "Invalid organizer; already created organizer " + find_duplicates.name
            raise HTTPException(status_code=400, detail=error_message)


        org_id = connection.execute(sqlalchemy.text(
            """
                INSERT INTO organizations (name, city)
                VALUES (:name, :city)
                RETURNING org_id
            """
        ), [{"name": new_organization.name, 
             "city": new_organization.city}]).scalar()

    if org_id != None:
        return {"org_id": org_id, 
                "name": new_organization.name, 
                "city": new_organization.city}
    else:
        error_message = "Invalid creating of organizer"
        raise HTTPException(status_code=400, detail=error_message)
    
@router.post("/{organization_id}/edit")
def edit_organization(organization_id: int, name: str = None, city: str = None):
    """ 
    """
    set_clause = {}
    if name != None:
        set_clause["name"] = name
    if city != None:
        set_clause["city"] = city
    if name == None and city == None:
        error_message = "No information to edit organization"
        raise HTTPException(status_code=400, detail=error_message)
    
    set_clause_sql = ", ".join([f"{key} = :{key}" for key in set_clause.keys()])

# ! CHECK IF THIS IS BAD AND HOW TO FIX FOR SQL INJECTIONS
    with db.engine.begin() as connection:
        org_id = connection.execute(sqlalchemy.text(
            f"""
                UPDATE organizations
                SET {set_clause_sql}
                WHERE org_id = :organization_id
                RETURNING org_id
            """
        ), {"organization_id": organization_id, **set_clause}).scalar()

    if org_id != None:
        set_clause["org_id"] = org_id
        return set_clause
    else:
        error_message = "Invalid editing of organizer"
        raise HTTPException(status_code=400, detail=error_message)

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
        error_message = "Invalid creating of supervisor"
        raise HTTPException(status_code=400, detail=error_message)
    
@router.post("/supervisor/{supervisor_id}/edit")
def edit_supervisor(supervisor_id: int, organization_id: int = None, supervisor_name: str = None, email: str = None):
    """ """
    set_clause = {}
    if organization_id != None:
        set_clause["org_id"] = organization_id
    if supervisor_name != None:
        set_clause["sup_name"] = supervisor_name
    if email != None:
        set_clause["email"] = email
    if organization_id == None and supervisor_name == None and email == None:
        error_message = "No information to edit supervisor"
        raise HTTPException(status_code=400, detail=error_message)
    
    set_clause_sql = ", ".join([f"{key} = :{key}" for key in set_clause.keys()])

# ! CHECK IF THIS IS BAD AND HOW TO FIX FOR SQL INJECTIONS
    with db.engine.begin() as connection:
        sup_id = connection.execute(sqlalchemy.text(
            f"""
                UPDATE supervisors
                SET {set_clause_sql}
                WHERE sup_id = :supervisor_id
                RETURNING sup_id
            """
        ), {"supervisor_id": supervisor_id, **set_clause}).scalar()

    if sup_id != None:
        set_clause["sup_id"] = sup_id
        return set_clause
    else:
        error_message = "Invalid editing of supervisor"
        raise HTTPException(status_code=400, detail=error_message)
