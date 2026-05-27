from sqlalchemy.orm import Session

from app.core.models import ProducerModel
from app.manufacturers.domain.entity import ManufacturerEntity


class ManufacturerRepository:
    def __init__(self, db: Session):
        self._db = db

    def _to_entity(self, model: ProducerModel) -> ManufacturerEntity:
        return ManufacturerEntity(id=model.id, name=model.name)

    def list_all(self) -> list[ManufacturerEntity]:
        models = self._db.query(ProducerModel).order_by(ProducerModel.name).all()
        return [self._to_entity(m) for m in models]

    def get_by_id(self, producer_id: int) -> ManufacturerEntity | None:
        model = self._db.query(ProducerModel).filter(ProducerModel.id == producer_id).first()
        return self._to_entity(model) if model else None
