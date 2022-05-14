from . import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    pass_secure = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return AttributeError('Password cannot be read')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password, method='sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.pass_hashed, password)


@login.user_loader
def load_user(user_id):
    return User.get(user_id)


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    cover_image = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.title
