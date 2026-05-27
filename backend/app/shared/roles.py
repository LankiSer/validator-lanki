CLIENT = "client"
MANAGER = "manager"
ADMIN = "admin"
GUEST = "guest"


def can_filter_sort_search(role: str | None) -> bool:
    return role in {MANAGER, ADMIN}


def can_manage_products(role: str | None) -> bool:
    return role == ADMIN


def can_view_orders(role: str | None) -> bool:
    return role in {MANAGER, ADMIN}


def can_manage_orders(role: str | None) -> bool:
    return role == ADMIN
