from fastapi import FastAPI, Depends , Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlmodel import Session , select
from contextlib import asynccontextmanager
from database import ItemData , create_db_and_tables, get_session





SessionDep = Annotated[Session, Depends(get_session)]



@asynccontextmanager
async def lifespan(app: FastAPI):
    # create all tables 
    create_db_and_tables()
    yield
    


app = FastAPI(title="FastApi app here",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for local dev; list real origins in production
    allow_methods=["*"],
    allow_headers=["*"],
)





# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None







@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/items")
def create_items(item: ItemData, session: SessionDep) -> ItemData:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/api/items")
def all_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,          
) -> list[ItemData]:
    items = session.exec(select(ItemData).offset(offset).limit(limit)).all()
    return items
    





# @app.post("/upload/")
# def upload_file():
#     pass
