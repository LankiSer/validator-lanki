from fastapi import HTTPException, UploadFile, status

from app.categories.infra.repository import CategoryRepository
from app.products.app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.products.infra.repository import ProductRepository
from app.shared.storage import save_upload


class ProductService:
    def __init__(self, repo: ProductRepository, category_repo: CategoryRepository):
        self._repo = repo
        self._category_repo = category_repo

    def list_products(self, category_id: int | None = None) -> list[ProductResponse]:
        items = self._repo.list_all(category_id)
        return [ProductResponse(**p.__dict__) for p in items]

    def get_product(self, product_id: int) -> ProductResponse:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
        return ProductResponse(**product.__dict__)

    def create(self, data: ProductCreate) -> ProductResponse:
        self._ensure_category(data.category_id)
        product = self._repo.create(data.model_dump())
        return ProductResponse(**product.__dict__)

    def update(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        payload = data.model_dump(exclude_unset=True)
        if "category_id" in payload:
            self._ensure_category(payload["category_id"])
        product = self._repo.update(product_id, payload)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
        return ProductResponse(**product.__dict__)

    def delete(self, product_id: int) -> None:
        if not self._repo.delete(product_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")

    async def upload_image(self, product_id: int, file: UploadFile) -> ProductResponse:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")

        image_url = await save_upload(file)
        updated = self._repo.update(product_id, {"image_url": image_url})
        return ProductResponse(**updated.__dict__)

    def _ensure_category(self, category_id: int) -> None:
        if not self._category_repo.get_by_id(category_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Категория не найдена")
