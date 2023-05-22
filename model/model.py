from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, JSON, Column, VARCHAR


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
    pass
#hi
