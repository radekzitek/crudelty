from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class TimestampSchema(BaseModel):
    CreatedAt: Optional[datetime] = None
    UpdatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True) 