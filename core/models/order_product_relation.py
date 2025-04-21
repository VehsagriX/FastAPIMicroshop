from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProductRelation(Base):
    __tablename__ = "order_product_relation"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    unit_price: Mapped[int] = mapped_column(default=0, server_default="0")

    # association between Relation -> Order
    order: Mapped["Order"] = relationship(back_populates="products_details")

    # association between Relation -> Product
    product: Mapped["Product"] = relationship(back_populates="orders_details")
