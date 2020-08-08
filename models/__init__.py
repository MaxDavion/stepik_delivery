from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# orders_meals_association = db.Table('orders_meals',
#     db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
#     db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'))
# )