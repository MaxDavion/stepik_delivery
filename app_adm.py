from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'userz'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))


class Order(db.Model):
    __tablename__ = 'orders'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500))
    email = db.Column(db.String(50))


class Client(db.Model):
    __tablename__ = 'clients'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))


db.create_all()

mock_users = []
mock_users.append(User(name="Alex", email="alex@gmail.com"))
mock_users.append(User(name="Darina", email="darina@gmail.com"))
mock_users.append(User(name="Prohor", email="prokhor@gmail.com"))
db.session.add_all(mock_users)
db.session.commit()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Client, db.session))

app.run(debug=True, port=5001)