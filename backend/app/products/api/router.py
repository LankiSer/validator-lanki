from fastapi import APIRouter, Depends, File, UploadFile

from app.deps import get_optional_user, get_product_service, require_admin
from app.products.app.schemas import (
    PickUpPointResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProviderResponse,
    UnitResponse,
)
from app.products.app.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/references/providers", response_model=list[ProviderResponse])
def list_providers(service: ProductService = Depends(get_product_service)):
    return service.list_providers()


@router.get("/references/units", response_model=list[UnitResponse])
def list_units(service: ProductService = Depends(get_product_service)):
    return service.list_units()


@router.get("/references/pick-up-points", response_model=list[PickUpPointResponse])
def list_pick_up_points(service: ProductService = Depends(get_product_service)):
    return service.list_pick_up_points()


@router.get("", response_model=list[ProductResponse])
def list_products(
    search: str | None = None,
    producer_id: int | None = None,
    manufacturer_id: int | None = None,
    category_id: int | None = None,
    sort_by: str | None = None,
    sort_dir: str = "asc",
    user=Depends(get_optional_user),
    service: ProductService = Depends(get_product_service),
):
    role = user.role if user else None
    return service.list_products(
        role=role,
        search=search,
        producer_id=producer_id or manufacturer_id,
        category_id=category_id,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    return service.get_product(product_id)


@router.post("", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    _: object = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    return service.create(data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    _: object = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    return service.update(product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    _: object = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    service.delete(product_id)


@router.post("/{product_id}/photo", response_model=ProductResponse)
async def upload_photo(
    product_id: int,
    file: UploadFile = File(...),
    _: object = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    return await service.upload_photo(product_id, file)
