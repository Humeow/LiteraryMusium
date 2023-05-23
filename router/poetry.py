import datetime
import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, text, select
from sqlalchemy.exc import IntegrityError

from model.model import *
from db.db import engine

import gloVars

import time
import json

from commands.load_reply import *
from commands.foot_writing import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def gallery_first_writing(gallery):
    gallery_first_writing_list = {
        "dc": 1, "eb": 2, "wp": 3, "hd": 4, "gwanmoo": 5,
    }

    return gallery_first_writing_list[gallery]


@router.get("/gallery/{gallery}", response_class=RedirectResponse, status_code=302)
async def show_writing(request: Request, gallery):
    writing_id = gallery_first_writing(gallery)

    return f"/gallery/{gallery}/{writing_id}"


@router.get("/gallery/{gallery}/{writing_id}")
async def show_writing(request: Request, gallery, writing_id):
    with Session(engine) as session:

        statement = select(Writing).where(Writing.id == writing_id).where(Writing.gallery == gallery)
        results = session.exec(statement)

        resFetch = results.first()

        if resFetch is None:
            return None

        #foot_writing_dict_list = gloVars.foot_writing_dict_list
        foot_writing_dict_list = foot_writing_dict_list_func(gallery)

        reply_dict_list = load_reply(writing_id, gallery)

        resFetch.count += 1
        session.add(resFetch)
        session.commit()

        session.refresh(resFetch)

        now_writing_dict = {
            "id": writing_id,
            "gallery": gallery,
            "subject": resFetch.subject,
            "title": resFetch.title,
            "nickname": resFetch.nickname,
            "ip": resFetch.ip,
            "reply_num": len(reply_dict_list),
            "date": resFetch.date,
            "count": resFetch.count,  # 조회수
            "recommend": resFetch.recommend,  # 추천
            "unrecommend": resFetch.unrecommend,

            "content": resFetch.content,
            "chat_id": resFetch.chat_ids.split(","),
        }

        gallery_list = [
            ["DC", 'dc'],
            ["EB", 'eb'],
            ["WP", 'wp'],
            ["HD", 'hd'],
            ["허관무", 'gwanmu'],
        ]

        return templates.TemplateResponse("clear_last.html",
                                          {"request": request, "now_writing_dict": now_writing_dict, "gallery_list": gallery_list,
                                           "foot_writing_dict_list": foot_writing_dict_list, "reply_dict_list": reply_dict_list,
                                          "gallery_list_length": len(gallery_list), })


@router.get("/print", response_class=HTMLResponse)
async def print_main(request: Request):
    return templates.TemplateResponse("clear_last.html", {"request": request, "alert_message": ""})


@router.post("/recommend", response_class=RedirectResponse, status_code=302)
async def recommend_writing(request: Request, is_recommendation: int = Form(), writing_id: int = Form(), gallery: str = Form()):

    return f"/gallery/{gallery}/1"


@router.post("/write")
async def write_writing(request: Request,
                        writing_id: int = Form(default=0), gallery: str = Form(default="wp"), subject: str = Form(default="일반"),
                        title: str = Form(), nickname: str = Form(), ip: str = Form(), reply_num: int = Form(default=0),
                        date: str = Form(default=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")),
                        count: int = Form(default=0), recommend: int = Form(default=0), unrecommend: int = Form(default=0),
                        content: str = Form(), chat_ids: str = Form(default=""), secret: str = Form()):
    if secret != os.environ.get('LiteraryMusium_WRITE_SECRET'):
        return None

    with Session(engine) as session:

        if writing_id == 0:
            writing_inform = Writing(
                gallery=gallery, subject=subject, title=title, nickname=nickname, ip=ip,
                reply_num=reply_num, date=date, count=count, recommend=recommend, unrecommend=unrecommend,
                content=content.replace('\\n', '\n'), chat_ids=chat_ids
            )
        else:
            writing_inform = Writing(
                id=writing_id, gallery=gallery, subject=subject, title=title, nickname=nickname, ip=ip,
                reply_num=reply_num, date=date, count=count, recommend=recommend, unrecommend=unrecommend,
                content=content, chat_ids=chat_ids
            )

        session.add(writing_inform)
        session.commit()
        session.refresh(writing_inform)
