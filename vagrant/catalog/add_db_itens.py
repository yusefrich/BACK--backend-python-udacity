from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def add_Restaurants(newRestaurantName):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    newRestaurant = Restaurant(name=newRestaurantName[0])
    session.add(newRestaurant)
    session.commit()


def update_Restaurants(myRestaurant):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newRestaurant = session.query(Restaurant).filter_by(id=myRestaurant.id).one()
    newRestaurant.name = myRestaurant.name
    session.add(newRestaurant)
    session.commit()




