from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def delete_Restaurants(myRestaurantQuery):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    restaurant = session.query(Restaurant).filter_by(id=myRestaurantQuery.id).one()
    session.delete(restaurant)
    session.commit()

def delete_MenuItem(menu_id):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    session.delete(itemToDelete)
    session.commit()
