from fastapi import APIRouter, Depends
from apis.v1 import route_domain, route_user, route_llm, route_email, route_search
from auth.auth_bearer import JWTBearer

api_router = APIRouter()
# api_router.include_router(route_domain.router, prefix='/domain', tags=["domain"])
# api_router.include_router(route_user.router, prefix='/user', tags=["user"])
# api_router.include_router(route_email.router, prefix='/check', tags=["email"], include_in_schema=False)
# api_router.include_router(route_llm.router, prefix='/llm', tags=["llm"])
api_router.include_router(route_search.router, prefix='/search', tags=["search"])



