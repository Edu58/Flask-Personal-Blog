from . import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'authors'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    pass_secure = db.Column(db.String(), nullable=False)
    posts = db.relation('BlogPost', backref='author', lazy='dynamic')
    comments = db.relation('Comments', backref='author', lazy='dynamic')

    @property
    def password(self):
        return AttributeError('Password cannot be read')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password, method='sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)


@login.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    post_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    cover_image = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('authors.user_id'))

    def __repr__(self):
        return self.title

    def save_blogpost(self):
        db.session.add(self)
        db.session.commit()

    def delete_blogpost(self):
        db.session.delete(self)
        db.session.commit()


class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('blogposts.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('authors.user_id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
