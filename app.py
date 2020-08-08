import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_script import Manager
import forms
from flask_migrate import Migrate, MigrateCommand
from models import db
from models.meals import Meal
from models.categories import Category
from models.accounts import Account
from models.orders import Order
# from models.orders import Order
# from sqlalchemy.sql.expression import func
from datetime import datetime
from sqlalchemy.sql.expression import func


app = Flask(__name__)
SECRET_KEY = "randomstring"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.reflect(app=app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def main():
    categories = Category.query.order_by(func.random()).all()
    g = session.get('cart')
    meals = Meal.query.order_by(func.random()).all()
    return render_template(
        "main.html",
        categories=categories,
        meals=meals,
        is_user_login=session.get('account_id')
    )

@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            account = Account.query.filter_by(email=form.data['email']).first()
            if account and str(account.password) == form.data['password']:
                session["account_id"] = account.id
                return render_template('account.html', is_user_login=session.get('account_id'))
            else:
                flash("Такой пользователь уже существует.", "danger")
                form.errors.update({'login': "Неверное имя или пароль"})
    return render_template('login.html', form=form)


@app.route('/register/', methods=["POST", "GET"])
def register():
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            account = Account.query.filter_by(email=form.data['email']).first()
            if not account:
                Account.add_from_form(**form.data).commit()
                account = Account.query.filter_by(email=form.data['email']).first()
                session["account_id"] = account.id
                return render_template('main.html', is_user_login=session.get('account_id'))
            else:
                flash("Такой пользователь уже существует.", "danger")

    return render_template("register.html", form=form)


@app.route('/addtocart/<int:id>')
def addtocart(id):
    meal = Meal.query.filter_by(id=id).first()
    _meal = {"id": meal.id, "price": meal.price, "title": meal.title}
    _cart = session.get("cart", [])
    if _meal not in _cart:
        _cart.append({"id": meal.id, "price": meal.price, "title": meal.title})
    session['cart'] = _cart
    return redirect(url_for("main"))


@app.route('/delfromcart/<int:id>')
def delfromcart(id):
    _cart = session.get("cart", [])
    _cart.remove([i for i in _cart if i['id'] == id][0])
    session['cart'] = _cart
    return redirect(url_for("main"))

@app.route('/cart/', methods=["POST", "GET"])
def cart():
    form = forms.OrderForm()
    if request.method == 'POST':
        account = Account.query.filter_by(id=session['account_id']).first()
        if form.validate_on_submit():
            amount = sum([i['price'] for i in session['cart']])
            Order.add_from_form(**form.data, amount=amount, account=account).commit()
            session['cart'] = []
            return render_template("ordered.html")
    return render_template("cart.html", form=form)


@app.route('/account/')
def account():
    return render_template("account.html", is_user_login=session.get('account_id'))






@app.route('/logout/')
def logout():
    session.pop('account_id')
    return redirect(url_for("main"))


@app.route('/ordered/', methods=["POST", "GET"])
def ordered():
    return render_template(
        "ordered.html",
    )

if __name__ == '__main__':
    app.run(port=5001)