from typing import Annotated, Optional

from fastapi import Depends, Query
from sqlmodel import Session

from .database import engine


# TODO: add limit: Annotated[int, Query(le=100, ge=1)] = 10
# Common parameters for all endpoints
async def common_parameters(
        offset: int = Query(default=0, ge=0), 
        limit: int = Query(default=10, ge=1, le=100), 
        q: Optional[str] = Query(default=None, description="Search q")
        ):
    return {"offset": offset, "limit": limit, "q": q}

CommonsDep = Annotated[dict, Depends(common_parameters)]

# Session dependency for database operations
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
