from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

import os
import typing

from db.db import *


# from router import router_user_manage, router_card_search

# ========== default setting ================== #

def basic_db_setting(content):
    from sqlmodel import Session
    from model.model import Writing
    from datetime import datetime

    with Session(engine) as session:
        date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        for gallery in ['eb', 'dc', 'wp', 'hd', 'gwanmu']:
            writing_inform = Writing(id=1,
                                     gallery=gallery, subject="공지", title="메인화면", nickname="갤주", ip="127.0",
                                     reply_num=0, date=date, count=10000, recommend=10000, unrecommend=-10000,
                                     content=content.replace('\\n', '\n'), chat_ids=""
                                     )

            session.add(writing_inform)

        session.commit()
        session.refresh(writing_inform)


# ========== global_variable insert =========== #

if os.environ.get('LiteracyMusium_DOCS_ENABLE') == 'true':
    print("`/document_diminside` ENABLED")
    app = FastAPI(docs_url="/document_diminside", redoc_url=None)
else:
    app = FastAPI(docs_url=None, redoc_url=None)

for file in os.listdir("./router"):
    if len(file) >= 4:
        if file[-3:] == ".py":
            exec("from router import " + file[:-3], globals())
            exec(f"app.include_router({file[:-3]}.router)", globals())

# create_db_and_tables()

app.mount("/static/", StaticFiles(directory='static', html=True), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse, status_code=302)
async def main(request: Request):
    return "/gallery/wp"
    # return {"response": "Hello!"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    favicon_path = 'favicon.ico'
    return FileResponse(favicon_path)


if __name__ == "__main__":
    import uvicorn

    create_db_and_tables()

    #  basic_db_setting("메인 화면이에요.")

    uvicorn.run(host="localhost", app=app)
# uvicorn main:app --reload
