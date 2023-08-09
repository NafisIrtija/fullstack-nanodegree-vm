from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.pool import SingletonThreadPool

from flask import (Flask, render_template, request,
                   redirect, url_for, flash, jsonify)
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# CORS(app)

engine = create_engine('sqlite:///restaurantmenu.db',
                       poolclass=SingletonThreadPool)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def all_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('all_restaurants'))
    else:
        return render_template('add_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant Edited!")
        return redirect(url_for('all_restaurants'))
    return render_template('edit_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Deleted!")
        return redirect(url_for('all_restaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/', methods=['GET', 'POST'])
@app.route('/restaurant/<int:restaurant_id>/menu/', methods=['GET', 'POST'])
def show_restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def create_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], price=request.form['price'],
                            description=request.form['description'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New Item added!")
        return redirect(url_for('show_restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('add_menu_item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name'] if len(request.form['name']) != 0 else item.name
        item.price = request.form['price'] if len(request.form['price']) != 0 else item.price
        item.description = request.form['description'] if len(request.form['description']) != 0 else item.description
        session.add(item)
        session.commit()
        flash("Item Edited!")
        return redirect(url_for('show_restaurant_menu', restaurant_id=restaurant.id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item Deleted!")
        return redirect(url_for('show_restaurant_menu', restaurant_id=restaurant.id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/<int:restaurant_id>/JSON/')
@cross_origin()
def show_restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[item.serialize for item in items])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
