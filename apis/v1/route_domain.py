# from fastapi import APIRouter, Depends, Response, Request
# from sqlalchemy.orm import Session
#
# from db.session import get_db
# from schemas.domain import DomainCreate, DomainOut, DomainAssign
# from db.crud import db_domain
#
# router = APIRouter()
#
#
# @router.post("/create",
#              summary="Create a domain")
# async def create_domain(data: DomainCreate, db: Session = Depends(get_db)):
#     return db_domain.create(data, db)
#
#
# @router.get("/list", response_model=list[DomainOut], summary="List of active domains")
# async def list_domains(db: Session = Depends(get_db)):
#     domains = db_domain.get_active_domains(db)
#     return domains
#
#
# @router.post("/assign_domain",
#              summary="Assign user a domain")
# async def create_domain(request: DomainAssign, db: Session = Depends(get_db)):
#     return db_domain.assign_domain_to_user(request, db)