from sqlmodel import create_engine
import os

from sqlmodel import SQLModel

password = os.environ.get('LiteraryMusium_DBPW')

DATABASE = {
    'drivername': 'mysql',
    'host': '172.30.1.2',
    'port': '54333',
    'username': "humeow",
    'password': 'abcdefg0223',
    'query': {'charset': 'utf8'}
}

#url = "sqlite:///db/database.sqlite3"
# if os.environ.get('LiteraryMusium_DBPW') is not None:
#     url = f"postgresql://humeow0223:{password}@localhost:5432/literacy_musium"
# else:
#     #url = f"postgresql://humeow0223:{password}@diminside.humeow.xyz:54323/literacy_musium"
#     url = f"postgresql://humeow0223:{password}@127.141.95.127:54323/literacy_musium"

if os.environ.get('isDevelop') == 'true':
    url = f"postgresql://humeow0223:{password}@172.30.1.2:54333/literacy_musium"
elif os.environ.get('isDevelop') == 'dev':
    f"postgresql://humeow0223:{password}@localhost:54333/literacy_musium"
else:
    url = f"postgresql://humeow0223:{password}@localhost:54333/literacy_musium"

print(url)

engine = create_engine(
    url,
    #"mariadb://humeow0223:dodogomraspi0223!@125.141.95.127:6603/LiteracyMusium",
    #f"postgresql://humeow0223:{password}@diminside.humeow.xyz:54323/literacy_musium",
    echo=False
)


def create_db_and_tables():  # scooped_session?
    SQLModel.metadata.create_all(engine)

