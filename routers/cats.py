from fastapi import APIRouter, status

from .. import dependencies
from ..schemas import cats as schemas
from ..models.cats import Cat
from ..crud import cats as crud

router = APIRouter(prefix="/cats", tags=["cats"])

@router.get("/", response_model=list[schemas.CatRead])
async def get_cats(
    session: dependencies.SessionDep,
    commons: dependencies.CommonsDep
):
    return crud.get_cats(session, **commons)

@router.get("/{cat_id}", response_model=schemas.CatRead)
async def read_cat(
    cat_id: int, 
    session: dependencies.SessionDep):
    return crud.get_cat_by_id(session, cat_id)


@router.post("/", response_model=schemas.CatRead, status_code=status.HTTP_201_CREATED)
async def create_cat(cat: schemas.CatCreate, session: dependencies.SessionDep):
    return crud.create_cat(session, cat)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int, session: dependencies.SessionDep):
    crud.delete_cat(session, cat_id)
    return


@router.patch("/{cat_id}/salary", response_model=schemas.CatRead)
async def update_cat_salary(
    cat_id: int, 
    session: dependencies.SessionDep, 
    new_salary: schemas.CatUpdate
):
    return crud.update_cat_salary(session, cat_id, new_salary)
