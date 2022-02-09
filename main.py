from uuid import UUID

from fastapi import FastAPI
from fastapi.params import Depends
from redis import Redis
from rq import Queue, Worker
from sqlalchemy.orm import Session
import models
from models import SteuererklaerungCreateDto, SteuererklaerungDto
from repository import SteuererklaerungRepository
from database import SessionLocal, engine

models.BaseDbEntity.metadata.create_all(bind=engine)

redis = Redis()
q = Queue('steuer send', connection=redis)
worker = Worker([q], connection=redis, name='worker-foo')
workers = Worker.count(connection=redis)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def send_steuererklaerung(entity_id):
    # db = SessionLocal()
    # entity = SteuererklaerungRepository().get_by_id(db, entity_id)
    # print(entity.__str__)
    # entity = models.Status.success
    # result = SteuererklaerungRepository().create(db, entity)
    print(entity_id)


@app.get("/steuererklaerung")
def get_steuererklaerung(skip: int, limit: int, db: Session = Depends(get_db)):
    return SteuererklaerungRepository().get(db, skip, limit)


@app.get("/steuererklaerung/{id}")
def get_steuererklaerung(entity_id: UUID, db: Session = Depends(get_db)):
    return SteuererklaerungRepository().get_by_id(db, entity_id)


@app.post("/steuererklaerung", response_model=SteuererklaerungDto)
async def create_steuererklaerung(steuer: SteuererklaerungCreateDto, db: Session = Depends(get_db)):
    result = SteuererklaerungRepository().create(db, steuer)
    q.enqueue(send_steuererklaerung, result.id)
    # q.enqueue_at(datetime(2022, 2, 9, 19, 10), send_steuererklaerung, ident)
    # q.enqueue_in(timedelta(seconds=30), send_steuererklaerung, ident)
    return result
