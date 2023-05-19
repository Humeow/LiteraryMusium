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

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/gallery/{gallery}/{writing_id}")
async def show_writing(request: Request, gallery, writing_id):
    with Session(engine) as session:

        statement = select(Writing).where(Writing.id == writing_id).where(Writing.gallery == gallery)
        results = session.exec(statement)

        resFetch = results.first()

        print(resFetch)

        if resFetch is None:
            return None

        foot_writing_dict_list = gloVars.foot_writing_dict_list

        reply_dict_list = load_reply(writing_id)

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
    with Session(engine) as session:
        statement = select(Writing).where(Writing.id == writing_id)
        results = session.exec(statement)

        resFetch = results.first()

        if resFetch is None:
            return None

        if is_recommendation:
            resFetch.recommend += 1
        else:
            resFetch.unrecommend += 1


        session.add(resFetch)
        session.commit()

        session.refresh(resFetch)

    return f"/gallery/{gallery}/{writing_id}"
