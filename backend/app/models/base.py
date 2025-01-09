from datetime import datetime
from sqlalchemy import Column, DateTime
from ..core.db import Base

class TimestampMixin:
    """Mixin for adding timestamp fields to models"""
    CreatedAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 