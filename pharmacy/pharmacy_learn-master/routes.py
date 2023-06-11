import datetime
from flask import render_template,  url_for, request, flash, redirect
from app import app, db
from models import User, Item, Order, OrderItem
from flask_login import current_user, login_user, login_required, logout_user


from settings import *

@app.route("/") # Вказуємо url-адресу для виклику функції
def index():
    items = Item.query.all()
    return render_template("index.html", items = items)#Результат, що повертається у браузер

@app.route("/signup", methods=["POST", "GET"]) # Вказуємо url-адресу для виклику функції
def signup():
    if request.method == "POST":
        user =  User.query.filter_by(username=request.form['username']).first()
        if user:
            flash('Такий email вже існує!', category='alert-warning')
        elif request.form['password1'] == request.form['password2']:
            try:
                u = User(name = request.form['name'], username = request.form['username'])
                u.set_password(request.form['password1'])
                db.session.add(u)
                db.session.commit()
                flash('Реєстрація успішна! Увійдіть у свій профіль.', category='alert-success')
                return redirect(url_for('signin'))
            except:
                db.session.rollback()
        else:
            flash('Паролі не співпадають!', category='alert-danger')

    return render_template("signup.html")#Результат, що повертається у браузер


@app.route("/signin", methods = ["POST", "GET"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password'] ):
            # функція вносить інформацію про залогіненого користувача в сесії браузера
            if login_user(user, remember=True, duration = datetime.timedelta(days=15)): 
                return redirect(url_for('index')) # якщо успішно - переходимо на головну
            else:
                flash('Помилка', category='alert-danger')

        else:
            flash('Неправильний логін або пароль', category='alert-danger')
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з профілю', category='alert-warning')
    return redirect(request.args.get('next')  or url_for('signin'))

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/<username>')
def page(username):
    user = User.query.filter_by(username=username).first_or_404()   
    return render_template("userpage.html", user = user)

@app.errorhandler(404)
def error_404(err):
    return render_template('error404.html')


@app.route("/order/<item_id>")
@login_required
def order(item_id):
    user = User.query.get(current_user.id)
    order = Order.query.filter_by(user_id = current_user.id).first()
    if order == None:
        order = Order(user_id=current_user.id, adress='Lviv, Khotkevycha 99')
        db.session.add(order)
        db.session.commit()

    item = Item.query.get(int(item_id))
    orderItem = OrderItem.query.filter_by(order_id = order.id, item_id = item.id).first()
    if orderItem == None:
        orderItem = OrderItem(order_id = order.id, item_id = item.id, total_price = item.price, image = item.image, name = item.name, description = item.description)
        db.session.add(orderItem)
        db.session.commit()

    return render_template('order.html', item = item, orderItem = orderItem, order = order, user = user)

@app.route("/add", methods=["POST"])
@login_required
def add():
    orderItem = OrderItem.query.get(request.form['order_item_id'])
    orderItem.set_amount(request.form['order_item_amount'])
    item = Item.query.get(orderItem.item_id)
    user = User.query.get(current_user.id)
    order = Order.query.filter_by(user_id = current_user.id).first()
    orderItem.set_total_price(round(float(item.price) * int(orderItem.amount)))
    orderItem.image = item.image
    orderItem.name = item.name
    orderItem.description = item.description
    db.session.add(orderItem)
    db.session.commit()
    
    return render_template('order.html', item = item, orderItem = orderItem, order = order, user = user)


@app.route("/item/<item_id>")
def itemInfo(item_id):#currentItem):
    item = Item.query.get(int(item_id))
    return render_template('item.html', item = item)

@app.route("/cart")
@login_required
def cart():
    user = User.query.get(current_user.id)
    order = Order.query.filter_by(user_id = current_user.id).first()
    if order == None:
        order = Order(user_id=current_user.id, adress='Lviv, Khotkevycha 99')
        db.session.add(order)
        db.session.commit()

    orderItems = OrderItem.query.filter_by(order_id = order.id).all()
    subtotal = 0
    for item in orderItems:
        subtotal += item.total_price
    discount = round(subtotal * 0.05, 2)
    shipping = 75.99
    total = round(subtotal - discount + shipping, 2)
    return render_template('cart.html', orderItems = orderItems, order = order, user = user, subtotal = subtotal, discount = discount, shipping = shipping, total = total, )

@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    user = User.query.get(current_user.id)
    order = Order.query.filter_by(user_id = current_user.id).first()
    if order != None:
        OrderItem.query.filter_by(order_id = order.id).delete()
        Order.query.filter_by(user_id = current_user.id).delete()
        db.session.commit()

    return render_template('thanks.html', user = user)

def Plus(quantity):
    quantity+=1

