import requests
from typing import Annotated

from fastapi import FastAPI, Depends, Query, HTTPException, Body
from pydantic import Field, validator, ValidationError

from sqlmodel import Field, SQLModel, create_engine, Session, select

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlite_file_name = "cats.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class CatBase(SQLModel):
    name: str
    years_of_exp: int | None = Field(
        default=0,
        ge=0,
        le=20,
        description="Years of experience in cat-related activities",
    )
    breed: str = Field(
        description="Breed of the cat, must be a valid breed from The Cat API"
    )
    salary: float | None 

class Cat(CatBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    @validator("breed")
    def validate_breed(cls, value):
        if value:
            breed_API_URL = f"http://api.thecatapi.com/v1/breeds/{value}"
            response = requests.get(breed_API_URL)
            if response.status_code != 200:
                raise ValueError(f"Invalid breed: {value}")
        return value


class CatsPublic(CatBase):
    id: int


# class CatUpdate(SQLModel):
#     salary: float | None = Field(
#         default=None, ge=0, description="New salary for the cat"
#     )



class TargetBase(SQLModel):
    name: str
    country: str
    notes: str
    complete_state: bool = Field(
        default=False, description="Indicates if the target is complete or not"
    )


class Target(TargetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MissionBase(SQLModel):
    cat_id: int | None = Field(
        default=None,
        foreign_key="cat.id",
        description="ID of the cat assigned to the mission",
    )
    target_id: int | None = Field(
        default=None,
        foreign_key="target.id",
        description="ID of the target for the mission",
    )
    complete_state: bool = Field(
        default=False, description="Indicates if the mission is complete or not"
    )


class Mission(MissionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MissionCreate(SQLModel):
    cat_id: int | None = Field(
        default=None,
        foreign_key="cat.id",
        description="ID of the cat assigned to the mission",
    )
    taget: TargetBase
    complete_state: bool = False

    # @validator("cat_id")
    # def validate_cat_id(cls, value):
    #     if value <= 0:
    #         raise ValueError("cat_id must be a positive integer")

    #     return value


class MissionPublic(SQLModel):
    id: int
    cat: CatBase | None = None
    target: TargetBase | None = None
    complete_state: bool


class MissionUpdate(SQLModel):
    notes: str | None = Field(default=None, description="Notes for the mission")
    complete_state: bool = Field(
        default=False, description="Indicates if the mission is complete or not"
    )




@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# basic CRUD operations for cats


@app.get("/cats/", response_model=list[CatsPublic])
async def read_cats(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100, ge=1)] = 10,
):
    cats = session.exec(select(Cat).offset(offset).limit(limit)).all()
    return cats


@app.get("/cats/{cat_id}", response_model=CatsPublic)
async def read_cat(cat_id: int, session: SessionDep):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    return cat


@app.post("/cats/", response_model=CatsPublic)
async def create_cat(cat: CatBase, session: SessionDep):
    try:
        db_cat = Cat.model_validate(cat)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid cat breed")
    else:
        session.add(db_cat)
        session.commit()
        session.refresh(db_cat)
        return db_cat


@app.delete("/cats/{cat_id}")
async def delete_cat(cat_id: int, session: SessionDep):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    session.delete(cat)
    session.commit()
    return {"message": "Cat deleted successfully"}


@app.patch("/cats/{cat_id}", response_model=CatsPublic)
async def update_cat_salary(
    cat_id: int, 
    session: SessionDep, 
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


@app.get("/missions/", response_model=list[MissionPublic])
async def read_missions(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100, ge=1)] = 10,
):
    missions = session.exec(select(Mission).offset(offset).limit(limit)).all()
    return [
        MissionPublic(
            id=mission.id,
            cat=session.get(Cat, mission.cat_id),
            target=session.get(Target, mission.target_id),
            complete_state=mission.complete_state,
        )
        for mission in missions
    ]


@app.get("/missions/{mission_id}", response_model=MissionPublic)
async def read_mission(mission_id: int, session: SessionDep):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    return MissionPublic(
        id=mission.id,
        cat=session.get(Cat, mission.cat_id),
        target=session.get(Target, mission.target_id),
        complete_state=mission.complete_state,
    )


@app.post("/missions/", response_model=MissionPublic)
async def create_mission(mission: MissionCreate, session: SessionDep):
    db_cat = session.get(Cat, mission.cat_id)
    # create a target
    target = Target.model_validate(mission.taget)
    session.add(target)
    session.commit()
    session.refresh(target)

    # create a mission
    db_mission = Mission(
        cat_id=mission.cat_id,
        target_id=target.id,
        complete_state=mission.complete_state,
    )
    session.add(db_mission)
    session.commit()
    session.refresh(db_mission)

    return MissionPublic(
        id=db_mission.id,
        cat=db_cat,
        target=target,
        complete_state=db_mission.complete_state,
    )


@app.delete("/missions/{mission_id}")
async def delete_mission(mission_id: int, session: SessionDep):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(
            status_code=400, detail="Cannot delete mission with assigned cat"
        )
    session.delete(mission)
    session.commit()
    return {"message": "Mission deleted successfully"}


@app.patch("/missions/{mission_id}/assign_cat", response_model=MissionPublic)
async def update_mission_assign_cat(mission_id: int, cat_id: int, session: SessionDep):
    db_mission = session.get(Mission, mission_id)
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    db_cat = session.get(Cat, cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    db_mission.sqlmodel_update({"cat_id": cat_id})
    session.commit()
    session.refresh(db_mission)

    db_target = session.get(Target, db_mission.target_id)
    return MissionPublic(
        id=db_mission.id,
        cat=db_cat,
        target=db_target,
        complete_state=db_mission.complete_state,
    )


@app.patch("/missions/{mission_id}/target", response_model=MissionPublic)
async def update_mission_target(
    mission_id: int,
    session: SessionDep,
    complete_state: bool = Body(default=None),
    notes: str = Body(default=None),
):

    db_mission = session.get(Mission, mission_id)
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    db_target = session.get(Target, db_mission.target_id)

    # Change complete_state
    if complete_state is not None:
        db_target.complete_state = complete_state

        db_mission.complete_state = complete_state

    # Change notes
    if notes is not None:
        if db_target.complete_state or db_mission.complete_state:
            raise HTTPException(
                status_code=400, detail="Cannot update notes for a completed mission"
            )
        db_target.notes = notes

    session.commit()
    session.refresh(db_target)
    session.refresh(db_mission)

    db_cat = session.get(Cat, db_mission.cat_id) if db_mission.cat_id else None
    return MissionPublic(
        id=db_mission.id,
        cat=db_cat,
        target=db_target,
        complete_state=db_mission.complete_state,
    )
