from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base


if TYPE_CHECKING:
    from .order import Order
    from .order_product_relation import OrderProductRelation


class Product(Base):

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_relation",
    #     back_populates="products",
    # )

    orders_details: Mapped[list["OrderProductRelation"]] = relationship(
        back_populates="product",
    )
