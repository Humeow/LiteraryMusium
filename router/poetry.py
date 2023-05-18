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


@router.get("/dimigo/{writing_id}")
async def show_writing(request: Request, writing_id):
    with Session(engine) as session:

        statement = select(Writing).where(Writing.id == writing_id)
        results = session.exec(statement)

        resFetch = results.first()

        if resFetch is None:
            return None

        foot_writing_dict_list = gloVars.foot_writing_dict_list

        reply_dict_list = load_reply(writing_id)

        now_writing_dict = {
            "id": resFetch.id,
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

        return templates.TemplateResponse("clear_last.html",
                                          {"request": request, "now_writing_dict": now_writing_dict,
                                           "foot_writing_dict_list": foot_writing_dict_list, "reply_dict_list": reply_dict_list})


@router.get("/print", response_class=HTMLResponse)
async def print_main(request: Request):
    return templates.TemplateResponse("clear_last.html", {"request": request, "alert_message": ""})


@router.post("/recommend", response_class=RedirectResponse, status_code=302)
async def recommend_writing(request: Request, is_recommendation: int = Form(), writing_id: int = Form()):
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

    return f"/dimigo/{writing_id}"


@router.post("/dimigo/write/")
async def writing(request: Request, id: int, title: str,
                  content: str):
    with Session(engine) as session:
        cards_inform = Writing(
            id=id, title=title, content=content, chat_ids=""
        )

        session.add(cards_inform)
        session.commit()

        session.refresh(cards_inform)

