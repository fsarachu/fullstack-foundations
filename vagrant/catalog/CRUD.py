from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# --- CREATE ---

def crud_create():
    # New restaurant
    milanga_house = Restaurant(name='Milanga House')  # Create new object
    pizza_house = Restaurant(name='Pizza House')
    session.add(milanga_house)  # New object is now staged to be added to the database
    session.add(pizza_house)
    session.commit()  # Commit staged changes

    # New menu item
    pizza_napolitana = MenuItem(name='Napolitana', description='Tomato sauce, ham and cheese', course='Entree',
                                price='$1.00',
                                restaurant=pizza_house)
    milanesa_napolitana = MenuItem(name='Napolitana', description='Tomato sauce, ham and cheese', course='Entree',
                                   price='$2.99',
                                   restaurant=milanga_house)
    chicken = MenuItem(name='Pollo', description='Just chicken', course='Entree', price='$1.99',
                       restaurant=milanga_house)
    session.add(pizza_napolitana)
    session.add(milanesa_napolitana)
    session.add(chicken)
    session.commit()


def crud_read():
    # All restaurants and its items
    restaurants = session.query(Restaurant).all()

    for restaurant in restaurants:
        print '  - {} - '.format(restaurant.name)
        items = session.query(MenuItem).filter_by(restaurant=restaurant)
        for item in items:
            print '{} -> {}'.format(item.name, item.price)
        print '   -----------------   '


def crud_update():
    # Update pizza 'Napolitana' price

    napolitanas = session.query(MenuItem).filter_by(name='Napolitana')
    for napolitana in napolitanas:
        print 'At {}: {} -> {} [id {}]'.format(napolitana.restaurant.name, napolitana.name, napolitana.price,
                                               napolitana.id)
    # Ooops! We got two items with the same name! Let's get only the one from Pizza House
    pizza_napolitana = session.query(MenuItem).filter_by(id=3).one()
    print 'Old price: {}'.format(pizza_napolitana.price)

    pizza_napolitana.price = '$0.80'
    session.add(pizza_napolitana)
    session.commit()

    pizza_napolitana = session.query(MenuItem).filter_by(id=3).one()
    print 'New price: {}'.format(pizza_napolitana.price)


def crud_delete():
    pizza_house = session.query(Restaurant).filter_by(name='Pizza House').one()
    session.delete(pizza_house)
    session.commit()


if __name__ == '__main__':
    crud_create()
    crud_read()

    crud_update()
    crud_read()

    crud_delete()
    print '\nAfter delete:\n'
    crud_read()
