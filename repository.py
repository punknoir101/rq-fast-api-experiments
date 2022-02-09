from uuid import UUID

from sqlalchemy.orm import Session

from models import Status, Steuererklaerung, SteuererklaerungCreateDto, SteuererklaerungDto


class SteuererklaerungRepository:
    def get(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Steuererklaerung).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, entity_id: UUID):
        return db.query(Steuererklaerung).filter(Steuererklaerung.id == entity_id).first()

    def create(self, db: Session, dto: SteuererklaerungCreateDto):
        entity = Steuererklaerung(userId=dto.userId, payload=dto.payload, status=Status.new)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity_id: UUID):
        entity = db.query(Steuererklaerung).filter(Steuererklaerung.id == entity_id).first()
        db.delete(entity)
        db.commit()
        return True
