from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from core.config import settings
from db.base_class import Base



class LLM(Base):
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, nullable=True)
    api_base = Column(String, nullable=True)
    azure_deployment_model = Column(String, nullable=True)
    azure_embedding_model = Column(String, nullable=True)
    open_ai_version = Column(String, nullable=True)
    open_ai_type = Column(String)
    model_engine = Column(String)
    model_name = Column(String)
    icon_name = Column(String)
    model_token_limit = Column(Integer, default=0)
    output_token_limit = Column(Integer, default=0, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_visible = Column(Boolean, default=True)
