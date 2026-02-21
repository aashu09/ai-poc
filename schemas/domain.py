from typing import Union, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, EmailStr, StrictStr


class DomainCreate(BaseModel):
    domain_name: StrictStr
    search_index_name: StrictStr
    user_id: int
    is_active: bool = True


class DomainOut(BaseModel):
    id: int
    name: Union[str, None] = None
    is_active: bool
    search_index_name: Union[str, None] = None


class DomainAssign(BaseModel):
    domain_id: int
    user_id: int
