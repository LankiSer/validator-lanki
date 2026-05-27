from fastapi import APIRouter, Depends

from app.deps import get_manufacturer_service
from app.manufacturers.app.schemas import ManufacturerResponse
from app.manufacturers.app.service import ManufacturerService

router = APIRouter(prefix="/producers", tags=["producers"])


@router.get("", response_model=list[ManufacturerResponse])
def list_producers(service: ManufacturerService = Depends(get_manufacturer_service)):
    return service.list_all()
