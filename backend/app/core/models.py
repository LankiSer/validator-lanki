"""
Модели данных по ER-диаграмме экзамена (3NF).

Соответствие имён:
  Producer  -> producers       Provider -> providers
  Product   -> products        ProductInOrder -> product_in_order
  Order     -> orders          PickUpPoint -> pick_up_points
"""

from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(25), nullable=False)

    users = relationship("UserModel", back_populates="role")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False, default="")
    login = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("RoleModel", back_populates="users")
    orders = relationship("OrderModel", back_populates="user")

    @property
    def full_name(self) -> str:
        parts = [self.surname, self.name, self.patronymic]
        return " ".join(p for p in parts if p).strip()


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    products = relationship("ProductModel", back_populates="category")


class ProducerModel(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, nullable=False)

    products = relationship("ProductModel", back_populates="producer")


class ProviderModel(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, nullable=False)

    products = relationship("ProductModel", back_populates="provider")


class UnitModel(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), unique=True, nullable=False)

    products = relationship("ProductModel", back_populates="unit")


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    price = Column(Float, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    discount = Column(Float, default=0.0)
    amount_in_stock = Column(Float, default=0)
    description = Column(Text, default="")
    photo = Column(String(500), nullable=True)

    unit = relationship("UnitModel", back_populates="products")
    provider = relationship("ProviderModel", back_populates="products")
    producer = relationship("ProducerModel", back_populates="products")
    category = relationship("CategoryModel", back_populates="products")
    order_lines = relationship("ProductInOrderModel", back_populates="product")


class OrderStatusModel(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True, nullable=False)

    orders = relationship("OrderModel", back_populates="status")


class PickUpPointModel(Base):
    __tablename__ = "pick_up_points"

    id = Column(Integer, primary_key=True, index=True)
    post_code = Column(String(6), nullable=False)
    city = Column(String(30), nullable=False)
    street = Column(String(30), nullable=False)
    building = Column(String(6), nullable=False)

    orders = relationship("OrderModel", back_populates="pick_up_point")

    @property
    def full_address(self) -> str:
        return f"{self.post_code}, {self.city}, {self.street}, {self.building}"


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String(10), nullable=False)
    creation_date = Column(Date, default=date.today, nullable=False)
    delivery_date = Column(Date, nullable=False)
    pick_up_point_id = Column(Integer, ForeignKey("pick_up_points.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reception_code = Column(Integer, nullable=False)
    status_id = Column(Integer, ForeignKey("order_statuses.id"), nullable=False)

    user = relationship("UserModel", back_populates="orders")
    pick_up_point = relationship("PickUpPointModel", back_populates="orders")
    status = relationship("OrderStatusModel", back_populates="orders")
    lines = relationship("ProductInOrderModel", back_populates="order", cascade="all, delete")


class ProductInOrderModel(Base):
    __tablename__ = "product_in_order"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Integer, nullable=False, default=1)

    order = relationship("OrderModel", back_populates="lines")
    product = relationship("ProductModel", back_populates="order_lines")


# Алиасы для совместимости импортов в репозиториях
ManufacturerModel = ProducerModel
SupplierModel = ProviderModel
OrderItemModel = ProductInOrderModel
