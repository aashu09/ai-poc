from typing import Union, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, EmailStr, StrictStr


class UserCreate(BaseModel):
    first_name: StrictStr
    last_name: StrictStr
    email: EmailStr
    password: StrictStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    user_role: StrictStr
    is_active: bool


