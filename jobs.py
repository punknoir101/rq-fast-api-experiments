import models
from database import SessionLocal
from repository import SteuererklaerungRepository


def send_steuererklaerung(entity_id):
    db = SessionLocal()
    entity = SteuererklaerungRepository().get_by_id(db, entity_id)
    print(entity.__str__)
    setattr(entity, "status", models.Status.success)
    SteuererklaerungRepository().update(db, entity.id, entity)
    print(entity_id)
    return
