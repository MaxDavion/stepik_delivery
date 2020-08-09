from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Email, InputRequired, EqualTo


class LoginForm(FlaskForm):
    title = StringField('Stepik delivery')
    subtitle = StringField('Войдите, чтобы управлять')
    email = StringField("Электропочта", [Email(message="Неверный формат email")])
    password = PasswordField("Пароль", [Length(min=6, message="Пароль должен содержать не менее 6и символов")])
    submit = SubmitField('Войти')


class RegisterForm(LoginForm):
    subtitle = StringField('Создайте аккаунт')
    submit = SubmitField('Зарегистрироваться')
    confirm_password = PasswordField("Повторите пароль", [EqualTo('password', message='Введенные пароли не совпадают')])


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired(message="Поле обязательно для заполнения")])
    address = StringField('Адрес', [InputRequired(message="Поле обязательно для заполнения")])
    email = StringField("Электропочта", [Email(message="Неверный формат email")])
    phone = StringField("Телефон", [Length(min=7, message="Телефон должен содержать не менее 7 символов")])
    submit = SubmitField('Оформить заказ')

