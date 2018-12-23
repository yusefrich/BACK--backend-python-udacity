from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
print("============================== all the veggie burgers ==================================")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

print("============================== urban veggie burger ==================================")
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
print(UrbanVeggieBurger.price)
print("\n")

print("============================== update the urban veggie burger to 2.99 ==================================")
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

print("============================== new urban veggie burger price ==================================")
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
print(UrbanVeggieBurger.price)
print("\n")

print("============================== change all veggie burger prices to $2.99 ==================================")
for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

print("============================== all the veggie burgers ==================================")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")
