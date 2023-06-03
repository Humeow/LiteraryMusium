from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlmodel import UniqueConstraint, PrimaryKeyConstraint


class Replys(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
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

    id: Optional[int] = Field(default=None)
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
    link: str = Field(default=None)
    link_type: str = Field(default=None)
    chat_ids: str = Field(default="")


if __name__ == "__main__":
    pass
