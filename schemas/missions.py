from pydantic import BaseModel, Field
from typing import Optional

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete_state: bool = Field(
        default=False, description="Indicates if the target is complete or not"
    )


class TargetCreate(TargetBase):
    pass


class MissionCreate(BaseModel):
    complete_state: bool = False
    cat_id: Optional[int]
    target: TargetCreate


class MissionRead(BaseModel):
    id: int
    complete_state: bool
    cat_id: int | None = None
    
    target_name: str
    target_country: str
    target_notes: Optional[str] = None
    target_complete_state: bool = False

    class Config:
        orm_mode = True


class MissionUpdate(BaseModel):
    target_notes: Optional[str] = None
    complete_state: Optional[bool] = None
