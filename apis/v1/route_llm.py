# from fastapi import APIRouter, Depends, Response, Request
# from sqlalchemy.orm import Session
# from db.session import get_db
# from schemas.llm import LLMOut, LLMCreate, LLMList, LLMListNew
# from db.crud.llm import create_llm, get_llm
# from core.custom_exception import SystemException
# import logging
# from core.custom_status_code import custom_status
#
# logger = logging.getLogger("gunicorn.error")
#
# router = APIRouter()
#
# # @router.post("/create", response_model=LLMOut, summary="Create LLM")
# @router.post("/create", summary="Create LLM")
# async def create(llm_data: LLMCreate, db: Session = Depends(get_db)):
#     try:
#         llm = create_llm(llm_data, db)
#     except Exception as err:
#         logger.error(f"Error message - {err}")
#         raise SystemException(custom_status.CODE_DB_ERROR, str(err))
#     return llm
#
#
# @router.get("/list", response_model=list[LLMListNew], summary="LLM list")
# def get_llms(db: Session = Depends(get_db)):
#     try:
#         llm = get_llm(db)
#     except Exception as err:
#         logger.error(f"Error message - {err}")
#         raise SystemException(custom_status.CODE_DB_ERROR, str(err))
#     return llm
#
