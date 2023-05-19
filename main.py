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

# ========== global_variable insert =========== #

app = FastAPI(docs_url="/document_diminside", redoc_url=None)

for file in os.listdir("./router"):
    if len(file) >= 4:
        if file[-3:] == ".py":
            exec("from router import " + file[:-3], globals())
            exec(f"app.include_router({file[:-3]}.router)", globals())

# create_db_and_tables()

app.mount("/static/", StaticFiles(directory='static', html=True), name="static")
templates = Jinja2Templates(directory="templates")

create_db_and_tables()

@app.get("/", response_class=RedirectResponse, status_code=302)
async def main(request: Request):
    return "/gallery/wp/3"
    #return {"response": "Hello!"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    favicon_path = 'favicon.ico'
    return FileResponse(favicon_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(host="localhost", app=app)
# uvicorn main:app --reload
