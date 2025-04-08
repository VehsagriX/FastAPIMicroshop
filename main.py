import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings

from api_v1 import router as api_v1_router
from items.items_api import router as items_router
from users.user_api import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание БД

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(items_router)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
