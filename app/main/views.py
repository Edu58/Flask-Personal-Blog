from . import main
from app.models import BlogPost
from flask import render_template


@main.route('/')
def index():
    blogposts = BlogPost.query.all()
    return render_template('index.html', blogposts=blogposts)
