import locale
from flask import render_template, redirect, session, request, flash, url_for
from sqlalchemy.sql.expression import func
from app import app
from models.categories import Category
from models.accounts import Account
from models.meals import Meal
from models.orders import Order
import forms


@app.route('/')
def main():
    categories = Category.query.order_by(func.random()).all()
    meals = Meal.query.order_by(func.random()).all()
    return render_template(
        "main.html",
        categories=categories,
        meals=meals
    )

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if session.get('account_id'):
        return redirect(url_for("main"))

    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            _account = Account.query.filter_by(email=form.data['email']).first()
            if _account and _account.is_password_valid(form.data['password']):
                session["account_id"] = _account.id
                return render_template('account.html')
            else:
                flash("Неверная электропочта или пароль. ", "warning")

    return render_template('login.html', form=form)


@app.route('/register/', methods=["POST", "GET"])
def register():
    if session.get('account_id'):
        return redirect(url_for("main"))

    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            _account = Account.query.filter_by(email=form.data['email']).first()
            if not _account:
                Account.add_from_form(**form.data).commit()
                _account = Account.query.filter_by(email=form.data['email']).first()
                session["account_id"] = _account.id
                return redirect(url_for("main"))
            else:
                flash("Пользователь с такой почтой уже существует.", "warning")

    return render_template("register.html", form=form)


@app.route('/addtocart/<int:id>')
def addtocart(id):
    meal = Meal.query.filter_by(id=id).first()
    _meal = {"id": meal.id, "price": meal.price, "title": meal.title}
    _cart = session.get("cart", [])
    if _meal not in _cart:
        _cart.append({"id": meal.id, "price": meal.price, "title": meal.title})
        flash("Блюдо добавлено в корзину", "success")
    else:
        flash("Блюдо уже в корзине", "danger")
    session['cart'] = _cart
    return redirect(url_for("cart"))


@app.route('/delfromcart/<int:id>')
def delfromcart(id):
    _cart = session.get("cart", [])
    _cart.remove([i for i in _cart if i['id'] == id][0])
    session['cart'] = _cart
    flash("Блюдо удалено из корзины", "warning")
    return redirect(url_for("cart"))


@app.route('/cart/', methods=["POST", "GET"])
def cart():
    form = forms.OrderForm()
    if request.method == 'POST':
        account = Account.query.filter_by(id=session['account_id']).first()
        if form.validate_on_submit():
            meals = [Meal.query.filter_by(id=i['id']).first() for i in session['cart']]
            amount = sum([i.price for i in meals])
            Order.add_from_form(**form.data, amount=amount, account=account, meals=meals).commit()
            session['cart'] = []
            return render_template("ordered.html")
    return render_template("cart.html", form=form)


@app.route('/account/')
def account():
    if not session.get('account_id'):
        return redirect(url_for("main"))

    user = Account.query.filter_by(id=session['account_id']).first()
    orders = Order.query.filter_by(account=user).all()
    return render_template("account.html", orders=orders)


@app.route('/logout/')
def logout():
    session.pop('account_id')
    return redirect(url_for("main"))


@app.route('/ordered/', methods=["POST", "GET"])
def ordered():
    if not session.get('account_id'):
        return redirect(url_for("main"))

    return render_template(
        "ordered.html",
    )

@app.template_filter('as_day_month')
def as_day_month(datetime):
    """ Вернуть день недели """
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    return datetime.strftime("%d %B")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html'), 404


