from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def hello_world():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).order_by(MenuItem.name.asc())

    output = ''

    output += '<h1>{} menu:</h1>'.format(restaurant.name)
    output += '<ul>'

    for item in items:
        output += '<li>{} - {} - {}</li>'.format(item.name, item.description, item.price)

    output += '</ul>'

    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
