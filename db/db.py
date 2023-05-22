from sqlmodel import create_engine
import os

from sqlmodel import SQLModel

password = str()
if os.path.exists("login_information.txt"):
    password = list(map(lambda x: x.strip, open("login_information.txt").readlines()))

DATABASE = {
    'drivername': 'mysql',
    'host': '125.141.95.127',
    'port': '6603',
    'username': "humeow",
    'password': 'abcdefg0223',
    'query': {'charset': 'utf8'}
}

url = "sqlite:///db/database.sqlite3"

engine = create_engine(
    url,
    #"mariadb://humeow0223:dodogomraspi0223!@125.141.95.127:6603/LiteracyMusium",
    echo=True
)


def create_db_and_tables():  # scooped_session?
    SQLModel.metadata.create_all(engine)
