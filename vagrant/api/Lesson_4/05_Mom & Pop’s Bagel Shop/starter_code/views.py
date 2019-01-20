from models import Base, User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine, asc

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

engine = create_engine('sqlite:///bagelShop.db')
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))

#ADD @auth.verify_password here
@auth.verify_password
def verify_password(username, password):
    print "Looking for user %s" % username
    user = session.query(User).filter_by(username = username).first()
    print(user)

    if not user:
        print "User not found"
        return False
    elif not user.verify_password(password):
        print "Unable to verify password"
        return False
    else:
        g.user = user
        return True

#ADD a /users route here
@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print("missing arguments")
        abort(400)  # missing arguments
    if session.query(User).filter_by(username = username).first() is not None:
        print("user exists")
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/protected_resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' %g.user.username})


@app.route('/bagels', methods = ['GET','POST'])
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = session.query(Bagel).all()
        return jsonify(bagels = [bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = Bagel(name = name, description = description, picture = picture, price = price)
        session.add(newBagel)
        session.commit()
        return jsonify(newBagel.serialize)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
