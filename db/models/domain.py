from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
from datetime import timezone, datetime


class UserSearchIndex(Base):
    id = Column(Integer, primary_key=True, index=True)
    search_index_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))


class Domain(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    search_index_name = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    domain_users = relationship("DomainUsers", back_populates="domains")


class DomainUsers(Base):
    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domain.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    domains = relationship("Domain", back_populates="domain_users")

