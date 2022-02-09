from enum import Enum
from uuid import UUID

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as GUID

from database import BaseDbEntity


class Status(Enum):
    new = 0
    scheduled = 1
    processing = 2
    failed = 3
    success = 4


class Steuererklaerung(BaseDbEntity):
    __tablename__ = "steuererklaerungen"

    id = Column(GUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"), )
    userId = Column(String)
    payload = Column(String)
    status = Column(sqlalchemy.Enum(Status))
    
    
class SteuererklaerungDto(BaseModel):
    id: UUID
    userId: str
    payload: str
    status: Status

    class Config:
        orm_mode = True


class SteuererklaerungCreateDto(BaseModel):
    userId: str
    payload: str

    class Config:
        orm_mode = True

