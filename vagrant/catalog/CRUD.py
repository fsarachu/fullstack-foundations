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
    # All items from all restaurants
    items = session.query(MenuItem).all()
    for item in items:
        print 'At {}: {} -> {}'.format(item.restaurant.name, item.name, item.price)


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


if __name__ == '__main__':
    # crud_create()
    # crud_read()
    crud_update()
