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
    restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()

    output = ''

    output += '<h1>Restaurants List</h1>'
    output += '<ul>'

    for restaurant in restaurants:
        output += '<li><a href="/restaurants/{}">{}</a></li>'.format(restaurant.id, restaurant.name)

    output += '</ul>'

    return output


@app.route('/restaurants/<int:restaurant_id>/')
def single_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    output = ''

    if not restaurant:
        output += '<h1>Restaurant {} doesn&apos;t exists'.format(restaurant_id)
    else:
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).order_by(MenuItem.name.asc()).all()

        output += '<h1>{}&apos;s Menu</h1>'.format(restaurant.name)

        output += """
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
        """

        for item in items:
            output += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(item.name, item.description, item.price)

        output += """
            </tbody>
          </table>
        """

    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
