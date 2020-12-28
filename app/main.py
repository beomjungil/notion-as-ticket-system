from fastapi import FastAPI

from .routers import go, github

app = FastAPI()

app.include_router(go.router)
app.include_router(github.router)


@app.get("/")
async def root():
    return "Hello Bigger Applications!"
