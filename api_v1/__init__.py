from fastapi import APIRouter
from .products.products_api import router as products_router
from .demo_auth.auth_api import router as demo_auth_router

router = APIRouter()
router.include_router(products_router)
router.include_router(demo_auth_router)
