from fastapi import HTTPException
from sqlmodel import Session, select

from ..models.cats import Cat
from ..schemas import cats as schemas

def get_cats(db: Session, offset: int = 0, limit: int = 10, q: str | None = None):
    cats = db.exec(select(Cat).offset(offset).limit(limit)).all()
    return cats

def get_cat_by_id(db: Session, cat_id: int):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

def create_cat(db: Session, cat_data: schemas.CatCreate) -> Cat:
    cat = Cat(**cat_data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def delete_cat(db: Session, cat_id: int):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
    
def update_cat_salary(db: Session, cat_id: int, new_salary: schemas.CatUpdate) -> Cat:
    db_cat = db.get(Cat, cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    db_cat.salary = new_salary.salary
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat
