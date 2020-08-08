from models import db


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    picture = db.Column(db.String(100), nullable=False)

    category = db.relationship("Category")
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # orders = db.relationship('Order', secondary=orders_meals_association, back_populates='meals')


