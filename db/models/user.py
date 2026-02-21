from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from db.base_class import Base
from core import constants
from datetime import datetime, timezone


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    auth_token = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    user_role = Column(String, default=constants.ROLES[0])
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    is_synced = Column(Boolean, default=False)
