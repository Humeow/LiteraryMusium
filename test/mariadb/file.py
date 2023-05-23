from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlmodel import create_engine
import os
from sqlmodel import SQLModel


from sqlalchemy import ForeignKeyConstraint, UniqueConstraint, PrimaryKeyConstraint


DATABASE = {
    'drivername': 'mysql',
    'host': '125.141.95.127',
    'port': '6603',
    'username': "humeow",
    'password': 'abcdefg0223',
    'query': {'charset': 'utf8'}
}

url = "sqlite:///db/database.sqlite3"

engine = create_engine(
    #url,
    f"postgresql://humeow0223:{'password'}@localhost:5432/literacy_musium",  # pip: psycopg2
    echo=True
)


def create_db_and_tables():  # scooped_session?
    SQLModel.metadata.create_all(engine)



class Replys(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, unique=True)
    name: str
    password: str
    ip: str
    context: str
    date: str
    writing_id: int

    class Config:
        arbitrary_types_allowed = True


class Writing(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('id', 'gallery', name="unique_id_by_gallery"),
        PrimaryKeyConstraint('id', 'gallery', name="unique_id_by_gallery")
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    gallery: str
    subject: str
    title: str
    nickname: str
    ip: str
    date: str
    count: int
    recommend: int = Field(default=0)
    unrecommend: int = Field(default=0)

    content: str
    chat_ids: str = Field(default="")


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
