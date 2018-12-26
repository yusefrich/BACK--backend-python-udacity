from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from request_db_items import get_Restaurants, get_FirstRestaurant, get_MenuItens, get_MenuItem
from add_db_items import add_MenuItem, update_MenuItem
from delete_db_items import delete_MenuItem

app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = get_MenuItens(get_Restaurants(restaurant_id))
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = get_MenuItem(menu_id)
    return jsonify(MenuItem=item.serialize)


@app.route('/')
def restaurants():
    restaurants = get_Restaurants()
    output = ''
    for i in restaurants:
        if(i.id > 5):
            output += "<br>"
            output += i.name
            output += "<br>"
            output += i.id
            output += "<br>"
            output += "<br>"
    return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    return render_template('menu.html',
                           restaurant=get_Restaurants(restaurant_id),
                           items=get_MenuItens(get_Restaurants(restaurant_id)))


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        add_MenuItem(restaurant_id, request.form['name'], request.form['price'], request.form['description'])
        flash("NEW MENU ITEM CREATED!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        if request.form['name']:
            update_MenuItem(menu_id, request.form['name'])
            flash("MENU ITEM EDITED!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=get_MenuItem(menu_id))


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        delete_MenuItem(menu_id)
        flash("NEW MENU ITEM DELETED!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               item=get_MenuItem(menu_id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
