from fastapi import APIRouter, Depends

from app.categories.app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from app.categories.app.service import CategoryService
from app.deps import get_category_service, require_admin

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(service: CategoryService = Depends(get_category_service)):
    return service.list_categories()


@router.post("", response_model=CategoryResponse)
def create_category(
    data: CategoryCreate,
    _: object = Depends(require_admin),
    service: CategoryService = Depends(get_category_service),
):
    return service.create(data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    _: object = Depends(require_admin),
    service: CategoryService = Depends(get_category_service),
):
    return service.update(category_id, data)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    _: object = Depends(require_admin),
    service: CategoryService = Depends(get_category_service),
):
    service.delete(category_id)
