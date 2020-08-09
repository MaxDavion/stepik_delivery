from models import db
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"id={self.id} email={self.email}"

    @property
    def password(self):
        raise AttributeError("Чтение пароля запрещено")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_password_valid(self, password):
        return check_password_hash(self.password_hash, password)

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

