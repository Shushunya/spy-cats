from fastapi import APIRouter, status

from ..dependencies import SessionDep, CommonsDep
from ..schemas import missions as schemas
from ..crud import missions as crud

router = APIRouter(prefix="/missions", tags=["missions"])

@router.get("/", response_model=list[schemas.MissionRead])
async def get_missions(
    session: SessionDep,
    commons: CommonsDep
):
    return crud.get_missions(session, **commons)

@router.get("/{mission_id}", response_model=schemas.MissionRead)
async def get_mission(mission_id: int, session: SessionDep):
    return crud.get_mission_by_id(session, mission_id)

@router.post("/", response_model=schemas.MissionRead, status_code=status.HTTP_201_CREATED)
async def create_mission(mission: schemas.MissionCreate, session: SessionDep):
    return crud.create_mission(session, mission)

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission(mission_id: int, session: SessionDep):
    crud.delete_mission(session, mission_id)
    return

@router.patch("/{mission_id}/cat", response_model=schemas.MissionRead)
async def update_mission_assign_cat(mission_id: int, cat_id: int, session: SessionDep):
    return crud.update_mission_assign_cat(session, mission_id, cat_id)

@router.patch("/{mission_id}/notes", response_model=schemas.MissionRead)
async def update_mission_target_notes(mission_id: int, data: schemas.MissionUpdate, session: SessionDep):
    return crud.update_mission_notes(session, mission_id, data)
