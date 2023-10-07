import sqlalchemy as sq
import json
from sqlalchemy.orm import sessionmaker

from models import create_tables, Book, Stock, Shop, Sale, Publisher

bd_system = 'postgresql'
login = "postgres"
password = "postgres"
db = "postgres"
DSN = f'{bd_system}://{login}:{password}@localhost:5432/{db}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open("tests_data.json", 'r') as f:
    data = json.load(f)

for news in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[news['model']]
    session.add(method(id=news['pk'], **news.get('fields')))


session.commit()

publ_name = input('Ведите имя писателя или id для вывода: ')
if publ_name.isnumeric():
    for c in session.query(Publisher).filter(
            Publisher.id == int(publ_name)).all():
        print(c)
else:
    for c in session.query(Publisher).filter(
            Publisher.name.like(f'%{publ_name}%')).all():
        print(c)

session.close()
