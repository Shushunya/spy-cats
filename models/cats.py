from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.missions import Mission


class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
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

    mission: Optional["Mission"] = Relationship(back_populates="cat")
