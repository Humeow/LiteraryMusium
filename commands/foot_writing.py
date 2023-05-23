import gloVars
from db.db import engine
from sqlmodel import Session
from sqlmodel import select

from model.model import *


def foot_writing_dict_list_func(gallery: str):
    with Session(engine) as session:
        statement = select(Writing).where(Writing.gallery == gallery).limit(30)
        results = session.exec(statement)

        every_writing_dict = results.fetchall()

        foot_writing_dict_list = list()
        for each_writing_dict in every_writing_dict:
            chatid_len = each_writing_dict.chat_ids.split(",")
            if chatid_len == ['']: chatid_len = 0
            else: chatid_len = len(chatid_len)

            print(each_writing_dict)

            if [each_writing_dict.id, each_writing_dict.gallery] in gloVars.foot_writing_dict_except_ids:
                continue

            foot_writing_dict_list.append(
                {
                    "id": each_writing_dict.id,
                    "subject": each_writing_dict.subject,
                    "title": each_writing_dict.title,
                    "nickname": each_writing_dict.nickname,
                    "ip": each_writing_dict.ip,
                    "reply_num": chatid_len,
                    "date": each_writing_dict.date.replace(".", "-"),
                    "specific_date": each_writing_dict.date[5:10],
                    "count": each_writing_dict.count,  # 조회수
                    "recommend": each_writing_dict.recommend,  # 추천
                }
            )

    return foot_writing_dict_list[::-1]
