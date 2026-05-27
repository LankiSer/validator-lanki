from sqlalchemy.orm import Session

from app.core.models import PickUpPointModel, ProviderModel, UnitModel


class RefsRepository:
    def __init__(self, db: Session):
        self._db = db

    def list_providers(self) -> list[dict]:
        rows = self._db.query(ProviderModel).order_by(ProviderModel.name).all()
        return [{"id": r.id, "name": r.name} for r in rows]

    def list_units(self) -> list[dict]:
        rows = self._db.query(UnitModel).order_by(UnitModel.name).all()
        return [{"id": r.id, "name": r.name} for r in rows]

    def list_pick_up_points(self) -> list[dict]:
        rows = self._db.query(PickUpPointModel).order_by(PickUpPointModel.id).all()
        return [
            {
                "id": r.id,
                "post_code": r.post_code,
                "city": r.city,
                "street": r.street,
                "building": r.building,
                "full_address": r.full_address,
            }
            for r in rows
        ]

    def provider_exists(self, provider_id: int) -> bool:
        return self._db.query(ProviderModel).filter(ProviderModel.id == provider_id).count() > 0

    def unit_exists(self, unit_id: int) -> bool:
        return self._db.query(UnitModel).filter(UnitModel.id == unit_id).count() > 0

    def pick_up_point_exists(self, point_id: int) -> bool:
        return self._db.query(PickUpPointModel).filter(PickUpPointModel.id == point_id).count() > 0
