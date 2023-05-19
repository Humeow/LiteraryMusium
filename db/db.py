from sqlmodel import create_engine
import os

from sqlmodel import SQLModel

password = str()
if os.path.exists("login_information.txt"):
    password = list(map(lambda x: x.strip, open("login_information.txt").readlines()))

DATABASE = {
    'drivername': 'mysql',
    'host': 'svc.sel4.cloudtype.app',
    'port': '30529',
    'username': "humeow",
    'password': 'abcdefg0223',
    'query': {'charset': 'utf8'}
}

url = "sqlite:///db/database.sqlite3"

engine = create_engine(
    url,
    #"mariadb://humeow:abcdefg0223@svc.sel4.cloudtype.app:30529/literacy",
    echo=True
)


def create_db_and_tables():  # scooped_session?
    SQLModel.metadata.create_all(engine)
