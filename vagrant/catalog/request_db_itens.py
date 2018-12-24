from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def get_Restaurants(myId = None):
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if myId is not None:
        restaurants = session.query(Restaurant).filter_by(id=myId).one()
        return restaurants
    else:
        restaurants = session.query(Restaurant).all()
        return restaurants


