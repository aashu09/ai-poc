from fastapi import HTTPException, status
from sqlalchemy.orm import load_only

from core import constants
from core.config import settings
from schemas.search import IndexCreate
from sqlalchemy.orm.session import Session
from db.models.index import Index


def create(request: IndexCreate, db: Session):
    # check if name is exist
    exists = db.query(Index).filter_by(Index_name=request.index_name).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'Index with given name:{request.index_name} already exist')
    if request.index_name == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'Index name is required')

    new_Index = Index(
        name=request.index_name,
        description=request.description,
    )
    db.add(new_Index)
    db.commit()
    db.refresh(new_Index)
    return new_Index


def get_indexs(db: Session):
    indexs = db.query(Index).all()
    return indexs

