import sys
from rq import Connection, Worker
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


with Connection():
    qs = sys.argv[1:] or ['steuer send']

    w = Worker(qs)
    w.work(with_scheduler=True)
