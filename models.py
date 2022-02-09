from uuid import UUID

from enum import Enum
from pydantic import BaseModel


class Status(Enum):
    new = 0
    scheduled = 1
    processing = 2
    failed = 3
    success = 4


class Steuererklaerung(BaseModel):
    id: UUID
    payload: str
    status: Status


class SteuererklaerungCreate(BaseModel):
    payload: str


def test_method():
    print("test method call")
