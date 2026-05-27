**Пример URL:**  
`GET /api/products?search=цемент&producer_id=1&sort_by=price&sort_dir=desc`
| Параметр | Что делает |
|----------|------------|
| `search` | Поиск по подстроке |
| `producer_id` | Фильтр по производителю |
| `category_id` | Фильтр по категории (в UI каталога нет) |
| `sort_by` | `price`, `discount`, `amount_in_stock` |
| `sort_dir` | `asc` или `desc` |

**Файл:** `backend/app/shared/roles.py`

CLIENT = "client"
MANAGER = "manager"
ADMIN = "admin"
GUEST = "guest"


def can_filter_sort_search(role: str | None) -> bool:
    return role in {MANAGER, ADMIN}

**Файл:** `backend/app/products/api/router.py`
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
**Файл:** `backend/app/products/app/service.py`
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
**Файл:** `backend/app/products/infra/repository.py`
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session, joinedload
from app.core.models import ProductModel, ProviderModel, UnitModel
def list_filtered(
    self,
    search: str | None = None,
    producer_id: int | None = None,
    category_id: int | None = None,
    sort_by: str | None = None,
    sort_dir: str = "asc",
) -> list[ProductEntity]:
    query = self._base_query()

    # --- ФИЛЬТРАЦИЯ (точное совпадение id) ---
    if producer_id:
        query = query.filter(ProductModel.producer_id == producer_id)
    if category_id:
        query = query.filter(ProductModel.category_id == category_id)

    # --- ПОИСК (подстрока в нескольких полях) ---
    if search:
        pattern = f"%{search.strip()}%"
        query = (
            query.join(ProductModel.provider)
            .join(ProductModel.unit)
            .filter(
                or_(
                    ProductModel.article.ilike(pattern),
                    ProductModel.name.ilike(pattern),
                    ProductModel.description.ilike(pattern),
                    ProviderModel.name.ilike(pattern),
                    UnitModel.name.ilike(pattern),
                )
            )
        )

    # --- СОРТИРОВКА ---
    sort_map = {
        "stock": ProductModel.amount_in_stock,
        "amount_in_stock": ProductModel.amount_in_stock,
        "price": ProductModel.price,
        "discount": ProductModel.discount,
    }
    column = sort_map.get(sort_by or "")
    if column is not None:
        direction = desc if sort_dir == "desc" else asc
        query = query.order_by(direction(column))
    else:
        query = query.order_by(ProductModel.id.asc())

    return [self._to_entity(m) for m in query.all()]
def _base_query(self):
    return self._db.query(ProductModel).options(
        joinedload(ProductModel.category),
        joinedload(ProductModel.producer),
        joinedload(ProductModel.provider),
        joinedload(ProductModel.unit),
    )
export function canFilterSortSearch() {
  return getRole() === ROLES.MANAGER || getRole() === ROLES.ADMIN
}
export function fetchProducts(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      query.append(key, value)
    }
  })
  const suffix = query.toString() ? `?${query}` : ''
  return api.get(`/products${suffix}`)
}
<template>
  <div class="toolbar card">
    <div v-if="canFilter" class="row">
      <div class="form-group grow">
        <label>Поиск</label>
        <input v-model="localSearch" class="input" placeholder="Артикул, название, описание..." />
      </div>
      <div class="form-group">
        <label>Производитель</label>
        <select v-model="localProducer" class="select">
          <option :value="null">Все производители</option>
          <option v-for="m in producers" :key="m.id" :value="m.id">{{ m.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Сортировка</label>
        <select v-model="localSort" class="select">
          <option value="">Без сортировки</option>
          <option value="amount_in_stock:asc">Количество ↑</option>
          <option value="amount_in_stock:desc">Количество ↓</option>
          <option value="price:asc">Цена ↑</option>
          <option value="price:desc">Цена ↓</option>
          <option value="discount:asc">Скидка ↑</option>
          <option value="discount:desc">Скидка ↓</option>
        </select>
      </div>
    </div>
    <p v-else class="muted">Гость и клиент видят список без поиска, сортировки и фильтрации.</p>
  </div>
</template>
import { computed, ref, watch } from 'vue'
import { canFilterSortSearch, canManageProducts } from '../../../store/auth'

const props = defineProps({ producers: Array, modelValue: Object })
const emit = defineEmits(['update:modelValue', 'add'])

const canFilter = computed(() => canFilterSortSearch())

const localSearch = ref(props.modelValue.search || '')
const localProducer = ref(props.modelValue.producer_id ?? null)
const localSort = ref(
  props.modelValue.sort_by
    ? `${props.modelValue.sort_by}:${props.modelValue.sort_dir || 'asc'}`
    : ''
)

watch([localSearch, localProducer, localSort], () => {
  const [sortBy, sortDir] = localSort.value ? localSort.value.split(':') : [null, 'asc']
  emit('update:modelValue', {
    search: localSearch.value,
    producer_id: localProducer.value,
    sort_by: sortBy,
    sort_dir: sortDir,
  })
})
import { fetchProducers } from '../../api/modules/manufacturers'
import { fetchProducts } from '../../api/modules/products'

const products = ref([])
const producers = ref([])
const filters = ref({ search: '', producer_id: null, sort_by: null, sort_dir: 'asc' })

async function load() {
  loading.value = true
  try {
    products.value = await fetchProducts(filters.value)
  } catch (err) {
    showError(err.message)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  producers.value = await fetchProducers()
  await load()
})

watch(filters, load, { deep: true })
<ProductToolbar v-model="filters" :producers="producers" @add="openAdd" />
```
Поля в ProductToolbar
  → filters { search, producer_id, sort_by, sort_dir }
  → fetchProducts(filters)
  → GET /api/products?search=...&producer_id=...
  → router → service (роль?) → list_filtered (SQL)
