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

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dimigo/{writiting_id}")
async def show_writing(request: Request, writiting_id):
    print(writiting_id)
    with Session(engine) as session:
        statement = select(Writing).where(Writing.id == writiting_id)
        results = session.exec(statement)

        resFetch = results.fetchall()[0]

        foot_writing_dict_list = gloVars.foot_writing_dict_list

        now_writing_dict = {
            "id": resFetch.id,
            "subject": resFetch.subject,
            "title": resFetch.title,
            "nickname": resFetch.nickname,
            "ip": resFetch.ip,
            "reply_num": resFetch.reply_num,
            "date": resFetch.date,
            "count": resFetch.count,  # 조회수
            "recommend": resFetch.recommend,  # 추천

            "content": resFetch.content,
            "chat_id": resFetch.chat_ids.split(","),
        }

        print(type(now_writing_dict))

        return templates.TemplateResponse("clear_last.html",
                                          {"request": request, "now_writing_dict": now_writing_dict,
                                           "foot_writing_dict_list": foot_writing_dict_list})


@router.get("/print", response_class=HTMLResponse)
async def print_main(request: Request):
    return templates.TemplateResponse("clear_last.html", {"request": request, "alert_message": ""})


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
