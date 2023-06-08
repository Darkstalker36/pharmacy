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


@app.route("/order")
def order():
    return render_template('order.html')

@app.route("/item/<item_id>")
def itemInfo(item_id):#currentItem):
    item = Item.query.get(int(item_id))
    return render_template('item.html', item = item)