from fastapi import APIRouter, Body

from .. import dependencies
from ..models.cats import Cat
from ..crud import cats as crud

router = APIRouter(prefix="/cats", tags=["cats"])

@router.get("/")
async def get_cats(
    session: dependencies.SessionDep,
    commons: dependencies.CommonsDep
):
    return crud.get_cats(session, **commons)

@router.get("/{cat_id}")
async def read_cat(
    cat_id: int, 
    session: dependencies.SessionDep):
    return crud.get_cat_by_id(session, cat_id)


@router.post("/", response_model=Cat)
async def create_cat(cat: Cat, session: dependencies.SessionDep):
    return crud.create_cat(session, cat)


@router.delete("/{cat_id}")
async def delete_cat(cat_id: int, session: dependencies.SessionDep):
    crud.delete_cat(session, cat_id)
    return


@router.patch("/{cat_id}", response_model=Cat)
async def update_cat_salary(
    cat_id: int, 
    session: dependencies.SessionDep, 
    new_salary: float = Body(default=None, gt=0)
):
    return crud.update_cat_salary(session, cat_id, new_salary)
