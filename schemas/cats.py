from pydantic import BaseModel, Field

class CatBase(BaseModel):
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

class CatCreate(CatBase):
    pass

class CatRead(CatBase):
    id: int

    class Config:
        orm_mode = True 

# class CatUpdate(BaseModel):
#     salary: float | None = Field(
#         default=None, ge=0, description="New salary for the cat"
#     )
