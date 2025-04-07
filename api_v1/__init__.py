from fastapi import APIRouter
from .products.products_api import router as products_router

router = APIRouter()
router.include_router(products_router)
