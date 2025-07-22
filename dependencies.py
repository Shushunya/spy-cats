from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from .database import get_session


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# List od dependencies
CommonsDep = Annotated[dict, Depends(common_parameters)] # Common parameters for all endpoints
SessionDep = Annotated[Session, Depends(get_session)] # Session dependency for database operations
