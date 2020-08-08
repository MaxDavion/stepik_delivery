from models import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # meals = db.relationship('Meal', secondary=orders_meals_association, back_populates='orders')
    #
    account = db.relationship("Account")
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    @classmethod
    def add_from_form(cls, **kwargs) -> 'Order':
        new_entry = cls(
            date=datetime.now(),
            amount=kwargs.get('amount'),
            state="Новый",
            email=kwargs.get('email'),
            phone=kwargs.get('phone'),
            address=kwargs.get('address'),
            account=kwargs.get('account')
            )
        db.session.add(new_entry)
        return new_entry

    def commit(self):
        db.session.commit()
