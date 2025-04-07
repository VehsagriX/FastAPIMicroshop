from pydantic import BaseModel, ConfigDict


class ProductsBase(BaseModel):
    name: str
    description: str
    price: int


class ProductsCreate(ProductsBase):
    pass


class Product(ProductsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
