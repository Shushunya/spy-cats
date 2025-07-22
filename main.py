from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import cats, missions
from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(cats.router)
app.include_router(missions.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
