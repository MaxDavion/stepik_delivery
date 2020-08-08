from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Length, Email, InputRequired


class LoginForm(FlaskForm):
    title = StringField('Stepik delivery')
    subtitle = StringField('Войдите, чтобы управлять')
    # email = StringField("Электропочта", [Email(message="Неверный формат email")])
    email = StringField("Электропочта", [Length(min=6, message="Неверный формат email")])
    password = StringField("Пароль", [Length(min=6, message="Пароль должен содержать не менее 6и символов")])
    submit = SubmitField('Войти')


class RegisterForm(LoginForm):
    subtitle = StringField('Создайте аккаунт')
    submit = SubmitField('Зарегистрироваться')


class OrderForm(FlaskForm):
    name = StringField('Ваше имя2', [InputRequired(message="Поле обязательно для заполнения")])
    address = StringField('Адрес', [InputRequired(message="Поле обязательно для заполнения")])
    # email = StringField("Электропочта", [Email(message="Неверный формат email")])
    email = StringField("Электропочта", [Length(min=6, message="Неверный формат email")])
    phone = StringField("Телефон", [Length(min=7, message="Телефон должен содержать не менее 7 символов")])
    submit = SubmitField('Оформить заказ')

