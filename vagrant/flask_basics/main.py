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
@app.route('/restaurants/')
def list_restaurants():
    restaurants = session.query(Restaurant).all()

    output = ''

    output += '<h1>Restaurants List</h1>'
    output += '<ul>'

    for restaurant in restaurants:
        output += '<li><a href="/restaurants/{}">{}</a></li>'.format(restaurant.id, restaurant.name)

    output += '</ul>'

    return output



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
