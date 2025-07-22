from ..models.missions import Mission
from ..models.cats import Cat
from fastapi import HTTPException
from ..schemas.missions import MissionCreate, MissionUpdate
from sqlmodel import Session, select

def get_missions(db: Session, offset: int = 0, limit: int = 10, q: str | None = None):
    missions = db.exec(select(Mission).offset(offset).limit(limit)).all()
    return missions

def get_mission_by_id(db: Session, mission_id: int):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

def create_mission(db: Session, mission_data: MissionCreate) -> Mission:
    mission = Mission(
        complete_state=mission_data.complete_state,
        cat_id=mission_data.cat_id,
        target_name=mission_data.target.name,
        target_country=mission_data.target.country,
        target_notes=mission_data.target.notes,
        target_complete_state=mission_data.target.complete_state
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

def delete_mission(db: Session, mission_id: int):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete assigned mission")
    
    db.delete(mission)
    db.commit()

def update_mission_assign_cat(db: Session, mission_id: int, cat_id: int) -> Mission:
    db_mission = db.get(Mission, mission_id)
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    db_cat = db.get(Cat, cat_id)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    
    db_mission.cat_id = db_cat.id
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission
    
def update_mission_notes(db: Session, mission_id: int, data: MissionUpdate) -> Mission:
    db_mission = db.get(Mission, mission_id)
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    new_notes = data.target_notes
    new_state = data.complete_state

    if new_notes is not None:
        if db_mission.complete_state or db_mission.target_complete_state:
            raise HTTPException(status_code=400, detail="Mission completed, no update allowed")
        
        db_mission.target_notes = new_notes

    if new_state is not None:
        db_mission.complete_state = new_state
        db_mission.target_complete_state = new_state
    
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission
