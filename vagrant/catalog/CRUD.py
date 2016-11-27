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
        print '{}: {}'.format(item.name, item.price)


if __name__ == '__main__':
    # crud_create()
    crud_read()
