from sqlmodel import create_engine, SQLModel
from .config import DB_URL


connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
