from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, JSON, Column


class Replys(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, unique=True)
    user: str
    password: str
    ip: str
    context: str
    date: str


class Writing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    subject: str
    title: str
    nickname: str
    ip: str
    reply_num: str
    date: str
    count: int
    recommend: int

    content: str
    chat_ids: str = Field(default="")


if __name__ == "__main__":
    pass