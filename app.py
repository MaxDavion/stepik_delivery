from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db
from models.meals import Meal
from models.categories import Category
from models.accounts import Account
from models.orders import Order


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
admin = Admin(app)

from views import *

admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))

if __name__ == '__main__':
    app.run(port=5001)