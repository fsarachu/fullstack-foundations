from flask import Flask
from flask import render_template

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
def restaurant_list():
    restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
    return render_template("restaurant_list.html", restaurants=restaurants)


@app.route('/restaurants/new/')
def restaurant_new():
    return render_template("restaurant_new.html")


@app.route('/restaurants/<int:restaurant_id>/edit/')
def restaurant_edit(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=id).first()

    if not restaurant:
        return render_template('404.html', http_response=404, msg='Restaurant {} doesn\'t exists'.format(id))
    else:
        return render_template('restaurant_edit.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/')
def restaurant_delete(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=id).first()

    if not restaurant:
        return render_template('404.html', http_response=404, msg='Restaurant {} doesn\'t exists'.format(id))
    else:
        return render_template('restaurant_delete.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    output = ''

    if not restaurant:
        output += '<h1>Restaurant {} doesn&apos;t exist.'.format(restaurant_id)
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


@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
