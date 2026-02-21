from fastapi import HTTPException, status
from sqlalchemy.orm import load_only

from core import constants
from core.config import settings

from schemas.domain import DomainCreate
from sqlalchemy.orm.session import Session
from db.models.user import Client


def get_client_details(client_id, db: Session):
    rows = db.query(Client).filter(Client.id == client_id).all()
    mylist = []
    for row in rows:
        item = {
            "id": row.id,
            "full_name": row.full_name,
            "email": row.email,
            "organization": row.organization,
            "assessment_id": row.assessment_id
        }
        mylist.append(item)

    return mylist

