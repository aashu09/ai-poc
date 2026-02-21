from fastapi import HTTPException, status
from sqlalchemy.orm import load_only

from core import constants
from core.config import settings
from schemas.domain import DomainCreate
from sqlalchemy.orm.session import Session
from db.models.domain import Domain, DomainUsers
from db.models.user import User


def create(request: DomainCreate, db: Session):
    # check if name is exist
    exists = db.query(Domain).filter_by(name=request.domain_name).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'Domain with given name:{request.domain_name} already exist')
    if request.domain_name == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'domain name is required')

    if request.search_index_name == "" or (not request.search_index_name):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'assessment_id is required')

    new_domain = Domain(
        name=request.domain_name,
        is_active=request.is_active,
        search_index_name = request.search_index_name,
        created_by=request.user_id
    )
    db.add(new_domain)
    db.commit()
    db.refresh(new_domain)
    return new_domain


def assign_domain_to_user(request, db:Session):
    exists = db.query(DomainUsers).filter_by(domain_id=request.domain_id, user_id= request.user_id).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'Domain already assigned')
    assign_domain = DomainUsers(
        domain_id=request.domain_id,
        user_id=request.user_id,
    )
    db.add(assign_domain)
    db.commit()
    db.refresh(assign_domain)
    return assign_domain


def get_active_domains(db: Session):
    domains = db.query(Domain).filter_by(is_active = True).all()
    return domains


def get_search_index_by_user(user, db:Session):
    responses = db.query(DomainUsers).join(User).filter(User.email==user).first()
    if responses:
        search_index = db.query(Domain).filter(Domain.id == responses.domain_id).first()
        return search_index
    else:
        return []
