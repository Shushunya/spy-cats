from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.cats import Cat

def get_cats(db: Session, offset: int = 0, limit: int = 10, q: str | None = None):
    cats = db.exec(select(Cat).offset(offset).limit(limit)).all()
    return cats

def get_cat_by_id(db: Session, cat_id: int):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

# TODO: add validation for cat breed
def create_cat(db: Session, cat: Cat):
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
    
def update_cat_salary(db: Session, cat_id: int, new_salary: float):
    db_cat = db.get(Cat, cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    db_cat.sqlmodel_update({"salary": new_salary})
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat
