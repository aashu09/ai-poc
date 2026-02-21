# from fastapi import APIRouter, Depends, Response, Request, status
# from sqlalchemy.orm import Session
#
# from db.models.user import User
# from db.session import get_db
# from fastapi.responses import JSONResponse
#
#
# router = APIRouter()
#
#
# @router.get("/email", response_model=None, summary="Check email already exists")
# async def list_domains(email: str, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == email.lower()).first()
#     if db_user:
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Email already exists")
#     else:
#         return JSONResponse(status_code=status.HTTP_200_OK, content="valid email")