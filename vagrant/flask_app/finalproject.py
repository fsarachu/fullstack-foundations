from flask import Flask
from flask import flash
from flask import jsonify
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
def showRestaurants():
    restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'GET':
        return render_template("newrestaurant.html")
    elif request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()

        flash('New Restaurant Created')

        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        if request.method == 'GET':
            return render_template('editrestaurant.html', restaurant=restaurant)
        elif request.method == 'POST':
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()

            flash('Restaurant Successfully Edited')

            return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template('404.html', msg='Restaurant {} doesn\'t exist'.format(restaurant_id))
    else:
        if request.method == 'GET':
            return render_template('deleterestaurant.html', restaurant=restaurant)
        elif request.method == 'POST':
            session.delete(restaurant)
            session.commit()

            flash('Restaurant Successfully Deleted')

            return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).order_by(MenuItem.name.asc()).all()
        return render_template("menu.html", restaurant=restaurant, menu=menu)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        if request.method == 'GET':
            return render_template("newmenuitem.html", restaurant=restaurant)
        elif request.method == 'POST':
            new_item = MenuItem(name=request.form['name'], description=request.form['description'],
                                price=request.form['price'], course=request.form['course'], restaurant=restaurant)
            session.add(new_item)
            session.commit()

            flash('Menu Item Created')

            return redirect(url_for('showMenu', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()

        if not item:
            return render_template("404.html", msg='Item {} doesn\'t exist'.format(restaurant_id)), 404
        else:
            if request.method == 'GET':
                return render_template("editmenuitem.html", restaurant=restaurant, item=item)
            elif request.method == 'POST':
                item.name = request.form['name']
                item.description = request.form['description']
                item.price = request.form['price']
                item.course = request.form['course']
                session.add(item)
                session.commit()

                flash('Menu Item Successfully Edited')

                return redirect(url_for('showMenu', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return render_template("404.html", msg='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()

        if not item:
            return render_template("404.html", msg='Item {} doesn\'t exist'.format(restaurant_id)), 404
        else:
            if request.method == 'GET':
                return render_template("deletemenuitem.html", restaurant=restaurant, item=item)
            elif request.method == 'POST':
                session.delete(item)
                session.commit()

                flash('Menu Item Successfully Deleted')

                return redirect(url_for('showMenu', restaurant_id=restaurant_id))


# API endpoints
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return jsonify(Error='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).order_by(MenuItem.name.asc()).all()
        return jsonify(MenuItems=[item.serialize for item in menu])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        return jsonify(Error='Restaurant {} doesn\'t exist'.format(restaurant_id)), 404
    else:
        item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()

        if not item:
            return jsonify(Error='Item {} doesn\'t exist'.format(menu_id)), 404
        else:
            return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = '5UP3R53CR37'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
