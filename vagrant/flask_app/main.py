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
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', http_response=404, msg='Restaurant {} doesn\'t exists'.format(id))
    else:
        return render_template('restaurant_edit.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/')
def restaurant_delete(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', http_response=404, msg='Restaurant {} doesn\'t exists'.format(id))
    else:
        return render_template('restaurant_delete.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exists'.format(restaurant_id))
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).order_by(MenuItem.name.asc()).all()
        return render_template("restaurant_menu.html", restaurant=restaurant, menu=menu)


@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def restaurant_menu_new(restaurant_id):
    return render_template("menu_new.html")


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
