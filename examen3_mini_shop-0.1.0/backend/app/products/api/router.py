from fastapi import APIRouter, Depends, File, UploadFile

from app.deps import get_product_service, require_admin
from app.products.app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.products.app.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def list_products(
    category_id: int | None = None,
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(category_id)


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


@router.post("/{product_id}/image", response_model=ProductResponse)
async def upload_image(
    product_id: int,
    file: UploadFile = File(...),
    _: object = Depends(require_admin),
    service: ProductService = Depends(get_product_service),
):
    return await service.upload_image(product_id, file)
