from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username= db.Column(db.String(50), nullable=False, unique=True)
    password= db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contact = db.relationship('Address', backref='info', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

        def __repr__(self):
            return f'<user{self.id} | {self.username}>'

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            db.session.add(self)
            db.session.commit()
        
    def __repr__(self):
        return f'<user{self.id} | {self.first_name}>'

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'first_name', 'last_name', 'phone_number', 'address'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()