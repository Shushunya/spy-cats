from sqlmodel import Field, SQLModel
from typing import Optional


# class CatBase(SQLModel):
#     name: str
#     years_of_exp: int | None = Field(
#         default=0,
#         ge=0,
#         le=20,
#         description="Years of experience in cat-related activities",
#     )
#     breed: str = Field(
#         description="Breed of the cat, must be a valid breed from The Cat API"
#     )
#     salary: float | None 


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

    # @validator("breed")
    # def validate_breed(cls, value):
    #     if value:
    #         breed_API_URL = f"http://api.thecatapi.com/v1/breeds/{value}"
    #         response = requests.get(breed_API_URL)
    #         if response.status_code != 200:
    #             raise ValueError(f"Invalid breed: {value}")
    #     return value

class CatUpdate(SQLModel):
    salary: float | None = Field(
        default=None, ge=0, description="New salary for the cat"
    )