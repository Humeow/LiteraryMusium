from sqlmodel import create_engine
import os

from sqlmodel import SQLModel

password = str()
if os.path.exists("login_information.txt"):
    password = list(map(lambda x: x.strip, open("login_information.txt").readlines()))

DATABASE = {
    'drivername': 'mysql',
    'host': 'aws.connect.psdb.cloud',
    'port': '3306',
    'username': "2v9y11k5phw2sdz5y15i",
    'password': password,
    'query': {'charset': 'utf8'}
}

url = "sqlite:///db/database.sqlite3"

engine = create_engine(
    url
)


def create_db_and_tables():  # scooped_session?
    SQLModel.metadata.create_all(engine)
