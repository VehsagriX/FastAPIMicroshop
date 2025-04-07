import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.models import Base, db_helper
from items.items_api import router as items_router
from users.user_api import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание БД
    async with db_helper.engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(items_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
