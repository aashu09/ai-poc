# from fastapi import APIRouter, Depends, Response, Request
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
#
# from db.session import get_db
# from db.crud import db_user
# from schemas.user import UserOut, UserCreate
# from fastapi_pagination import Page, paginate
#
# router = APIRouter()
#
#
# @router.post("/create", response_model=UserOut)
# def create_admin_user(user: UserCreate, db: Session = Depends(get_db)):
#     response = db_user.create_user(user, db)
#     return response
#
#
# @router.post("/login")
# def admin_login(form_data: UserCreate, db: Session = Depends(get_db)):
#     response = db_user.admin_login(form_data,db)
#     return response
#
#
# @router.get("/list", response_model=list[UserOut])
# def user_list( db: Session = Depends(get_db)):
#     response = db_user.get_user_list(db)
#     return response
