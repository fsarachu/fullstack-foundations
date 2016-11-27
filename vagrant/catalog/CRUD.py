from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# --- CREATE ---

def create():
    # New restaurant
    my_first_restaurant = Restaurant(name='Milanga House')  # Create new object
    session.add(my_first_restaurant)  # New object is now staged to be added to the database
    session.commit()  # Commit staged changes

    # New menu item
    napolitana = MenuItem(name='Napolitana', description='Tomato sauce, ham and cheese', course='Entree', price='$2.99',
                          restaurant=my_first_restaurant)
    chicken = MenuItem(name='Pollo', description='Just chicken', course='Entree', price='$1.99',
                       restaurant=my_first_restaurant)
    session.add(napolitana)
    session.add(chicken)
    session.commit()
