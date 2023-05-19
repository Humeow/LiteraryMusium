from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, text, select
from sqlalchemy.exc import IntegrityError

from model.model import *
from db.db import engine
from commands.makehash import hash_funcs

import gloVars

import time
import datetime
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

foot_writing_dict_list = gloVars.foot_writing_dict_list


@router.post("/reply", response_class=RedirectResponse, status_code=302)
async def show_writing(request: Request, writing_id: int = Form(), name: str = Form(), password: str = Form(),
                       content: str = Form(), gallery: str = Form()):
    with Session(engine) as session:
        statement = select(Writing).where(Writing.id == writing_id)
        results = session.exec(statement)

        resFetch = results.first()

        if resFetch is not None:
            now = datetime.datetime.now()
            reply_inform = Replys(
                name=name, ip=".".join(request.client.host.split(".")[:2]), password=hash_funcs.hash_make(password),
                context=content, date=now.strftime('%m.%d %H:%M:%S'), writing_id=writing_id
            )

            session.add(reply_inform)
            session.commit()
            session.refresh(reply_inform)

            statement = select(Writing).where(Replys.id == reply_inform.id)
            results = session.exec(statement)

            if len(resFetch.chat_ids):
                resFetch.chat_ids += ","

            resFetch.chat_ids += str(reply_inform.id)

            session.add(resFetch)
            session.commit()
            session.refresh(resFetch)

        return f"/gallery/{gallery}/{writing_id}"

        #return templates.TemplateResponse("clear_last.html",
        #                                  {"request": request, "now_writing_dict": now_writing_dict,
        #                                   "foot_writing_dict_list": foot_writing_dict_list})
