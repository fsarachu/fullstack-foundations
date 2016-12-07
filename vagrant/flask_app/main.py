from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
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


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def restaurant_new():
    if request.method == 'GET':
        return render_template("restaurant_new.html")
    elif request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()

        redirect(url_for('restaurant_list'))


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def restaurant_edit(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        if request.method == 'GET':
            return render_template('restaurant_edit.html', restaurant=restaurant)
        elif request.method == 'POST':
            pass


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        if request.method == 'GET':
            return render_template('restaurant_delete.html', restaurant=restaurant)
        elif request.method == 'POST':
            pass


@app.route('/restaurants/<int:restaurant_id>/menu/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).order_by(MenuItem.name.asc()).all()
        return render_template("restaurant_menu.html", restaurant=restaurant, menu=menu)


@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def menu_item_new(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        if request.method == 'GET':
            return render_template("menu_new.html", restaurant=restaurant)
        elif request.method == 'POST':
            pass


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def menu_item_edit(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()

        if not item:
            return render_template("404.html", msg='Item {} doesn\'t exist'.format(restaurant_id))
        else:
            if request.method == 'GET':
                return render_template("menu_edit.html", restaurant=restaurant, item=item)
            elif request.method == 'POST':
                pass


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def menu_item_delete(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()

        if not item:
            return render_template("404.html", msg='Item {} doesn\'t exist'.format(restaurant_id))
        else:
            if request.method == 'GET':
                return render_template("menu_delete.html", restaurant=restaurant, item=item)
            elif request.method == 'POST':
                pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
