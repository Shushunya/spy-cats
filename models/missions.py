from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .cats import Cat


class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    complete_state: bool = False

    cat_id: Optional[int] = Field(default=None, foreign_key="cat.id", unique=True, description="ID of the cat assigned to the mission")
    cat: Optional["Cat"] = Relationship(back_populates="mission")
    
    target_name: str
    target_country: str
    target_notes: Optional[str] = None
    target_complete_state: bool = False
