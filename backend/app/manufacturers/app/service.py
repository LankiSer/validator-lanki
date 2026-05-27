from app.manufacturers.app.schemas import ManufacturerResponse
from app.manufacturers.infra.repository import ManufacturerRepository


class ManufacturerService:
    def __init__(self, repo: ManufacturerRepository):
        self._repo = repo

    def list_all(self) -> list[ManufacturerResponse]:
        return [ManufacturerResponse(**m.__dict__) for m in self._repo.list_all()]
