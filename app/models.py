from . import db
from datetime import datetime


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
