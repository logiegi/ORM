import sqlalchemy as sq
import json

from select import select
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

def get_shops(res):
    answer = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale,
                           ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res.isdigit():
        c = answer.filter(Publisher.id == int(res)).all()
    else:
        c = answer.filter(Publisher.id.like(f'%{res}%')).all()
    for title, name, price, date_sale in c:
        print(f"{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")


if __name__ == '__main__':
    search = input('Ведите имя писателя или id для вывода: ')
    get_shops(search)
