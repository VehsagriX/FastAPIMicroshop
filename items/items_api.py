from typing import Annotated
from fastapi import APIRouter, Path

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/{item_id}/")
async def say_hello(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {"item": {
        "id": item_id,
    }}

