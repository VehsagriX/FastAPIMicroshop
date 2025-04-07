import uvicorn
from fastapi import FastAPI
from items.items_api import router as items_router
from users.user_api import router as users_router


app = FastAPI()

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
