from models import db


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


    @classmethod
    def add_from_form(cls, **kwargs) -> 'Account':
        new_entry = cls(
                email=kwargs.get('email'),
                password=kwargs.get('password')
            )
        db.session.add(new_entry)
        return new_entry

    def commit(self):
        db.session.commit()

