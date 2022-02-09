from uuid import UUID, uuid4
from typing import Optional
import sqlalchemy
import databases
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID as GUID

from models import Steuererklaerung, Status, SteuererklaerungCreate

DATABASE_URL = "postgresql://postgres:postgres@localhost/db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

steuererklaerungen = sqlalchemy.Table(
    "steuererklaerungen",
    metadata,
    sqlalchemy.Column("id", GUID, primary_key=True),
    sqlalchemy.Column("payload", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Enum(Status)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={}
)
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/steuererklaerung/{id}")
def get_steuererklaerung(id: UUID):
    steuer = Steuererklaerung(id=UUID('39599b34-d189-40ad-b1d8-0c7494f14313'), payload='payload', status=Status.new)

    return steuer


@app.post("/steuererklaerung", response_model=Steuererklaerung)
async def create_steuererklaerung(steuer: SteuererklaerungCreate):
    ident = uuid4()
    query = steuererklaerungen.insert().values(id=ident, payload=steuer.payload, status=Status.new)
    await database.execute(query)
    return {**steuer.dict(), "id": ident, "status": Status.new}
