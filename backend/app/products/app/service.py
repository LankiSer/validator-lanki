from fastapi import HTTPException, UploadFile, status

from app.categories.infra.repository import CategoryRepository
from app.manufacturers.infra.repository import ManufacturerRepository
from app.orders.infra.repository import OrderRepository
from app.products.app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.products.infra.refs_repository import RefsRepository
from app.products.infra.repository import ProductRepository
from app.shared.roles import can_filter_sort_search
from app.shared.storage import delete_upload, save_upload


class ProductService:
    def __init__(
        self,
        repo: ProductRepository,
        category_repo: CategoryRepository,
        producer_repo: ManufacturerRepository,
        order_repo: OrderRepository,
        refs_repo: RefsRepository,
    ):
        self._repo = repo
        self._category_repo = category_repo
        self._producer_repo = producer_repo
        self._order_repo = order_repo
        self._refs_repo = refs_repo

    def list_products(
        self,
        role: str | None,
        search: str | None = None,
        producer_id: int | None = None,
        category_id: int | None = None,
        sort_by: str | None = None,
        sort_dir: str = "asc",
    ) -> list[ProductResponse]:
        advanced = any([search, producer_id, sort_by])
        if advanced and not can_filter_sort_search(role):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Поиск, сортировка и фильтрация доступны менеджеру и администратору.",
            )

        items = self._repo.list_filtered(
            search=search if can_filter_sort_search(role) else None,
            producer_id=producer_id if can_filter_sort_search(role) else None,
            category_id=category_id,
            sort_by=sort_by if can_filter_sort_search(role) else None,
            sort_dir=sort_dir,
        )
        return [ProductResponse(**p.__dict__) for p in items]

    def list_providers(self) -> list[dict]:
        return self._refs_repo.list_providers()

    def list_units(self) -> list[dict]:
        return self._refs_repo.list_units()

    def list_pick_up_points(self) -> list[dict]:
        return self._refs_repo.list_pick_up_points()

    def get_product(self, product_id: int) -> ProductResponse:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
        return ProductResponse(**product.__dict__)

    def create(self, data: ProductCreate) -> ProductResponse:
        self._validate_refs(
            data.category_id,
            data.producer_id,
            data.provider_id,
            data.unit_id,
        )
        product = self._repo.create(data.model_dump())
        return ProductResponse(**product.__dict__)

    def update(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        current = self._repo.get_by_id(product_id)
        if not current:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
        payload = data.model_dump(exclude_unset=True)
        self._validate_refs(
            payload.get("category_id", current.category_id),
            payload.get("producer_id", current.producer_id),
            payload.get("provider_id", current.provider_id),
            payload.get("unit_id", current.unit_id),
        )
        product = self._repo.update(product_id, payload)
        return ProductResponse(**product.__dict__)

    def delete(self, product_id: int) -> None:
        if self._order_repo.product_in_orders(product_id):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Нельзя удалить товар: он присутствует в заказе.",
            )
        old_photo = self._repo.get_photo_path(product_id)
        if not self._repo.delete(product_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")
        delete_upload(old_photo)

    async def upload_photo(self, product_id: int, file: UploadFile) -> ProductResponse:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Товар не найден")

        old_photo = product.photo
        photo = await save_upload(file)
        updated = self._repo.update(product_id, {"photo": photo})
        delete_upload(old_photo)
        return ProductResponse(**updated.__dict__)

    def _validate_refs(
        self,
        category_id: int,
        producer_id: int,
        provider_id: int,
        unit_id: int,
    ) -> None:
        if not self._category_repo.get_by_id(category_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Категория не найдена")
        if not self._producer_repo.get_by_id(producer_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Производитель не найден")
        if not self._refs_repo.provider_exists(provider_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Поставщик не найден")
        if not self._refs_repo.unit_exists(unit_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Единица измерения не найдена")
