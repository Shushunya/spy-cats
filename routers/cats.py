from fastapi import APIRouter, HTTPException, Body
from sqlmodel import select
from pydantic import ValidationError


from .. import dependencies
from ..models.cats import Cat, CatBase

router = APIRouter(prefix="/cats", tags=["cats"])

@router.get("/")
async def get_cats(
    session: dependencies.SessionDep,
    commons: dependencies.CommonsDep
):
    cats = session.exec(select(Cat).offset(commons["skip"]).limit(commons["limit"])).all()
    return cats


@router.get("/{cat_id}")
async def read_cat(
    cat_id: int, 
    session: dependencies.SessionDep):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    return cat


@router.post("/", response_model=Cat)
async def create_cat(cat: CatBase, session: dependencies.SessionDep):
    try:
        db_cat = Cat.model_validate(cat)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid cat breed")
    else:
        session.add(db_cat)
        session.commit()
        session.refresh(db_cat)
        return db_cat


@router.delete("/{cat_id}")
async def delete_cat(cat_id: int, session: dependencies.SessionDep):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    session.delete(cat)
    session.commit()
    return {"message": "Cat deleted successfully"}


@router.patch("/{cat_id}", response_model=Cat)
async def update_cat_salary(
    cat_id: int, 
    session: dependencies.SessionDep, 
    new_salary: float = Body(default=None, gt=0)
):
    print(cat_id, new_salary)
    db_cat = session.get(Cat, cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    db_cat.sqlmodel_update({"salary": new_salary})
    session.add(db_cat)
    session.commit()
    session.refresh(db_cat)
    return db_cat
