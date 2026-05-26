from fastapi import HTTPException, status

from app.categories.app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from app.categories.infra.repository import CategoryRepository


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self._repo = repo

    def list_categories(self) -> list[CategoryResponse]:
        return [CategoryResponse(**c.__dict__) for c in self._repo.list_all()]

    def create(self, data: CategoryCreate) -> CategoryResponse:
        category = self._repo.create(data.name)
        return CategoryResponse(**category.__dict__)

    def update(self, category_id: int, data: CategoryUpdate) -> CategoryResponse:
        category = self._repo.update(category_id, data.name)
        if not category:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")
        return CategoryResponse(**category.__dict__)

    def delete(self, category_id: int) -> None:
        if not self._repo.delete(category_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")
