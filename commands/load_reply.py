from db.db import engine
from sqlmodel import Session
from sqlmodel import select

from model.model import *


def load_reply(writing_id: str, gallery: str):
    with Session(engine) as session:

        statement = select(Writing).where(Writing.id == writing_id).where(Writing.gallery == gallery)
        results = session.exec(statement)

        resFetch = results.first()
        if resFetch is None:
            return []

        if not len(resFetch.chat_ids) or resFetch.chat_ids == " ":
            return []

        chat_dict_list = list()
        for reply_id in resFetch.chat_ids.split(","):
            statement = select(Replys).where(Replys.id == reply_id)
            results = session.exec(statement)
            resFetch = results.first()

            if resFetch is None:
                continue

            chat_dict_list.append({
                "name": resFetch.name,
                "ip": resFetch.ip,
                "context": resFetch.context,
                "date": resFetch.date,
            })

    return chat_dict_list
