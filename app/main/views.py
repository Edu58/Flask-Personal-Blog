from . import main
from app import db
from app.models import BlogPost
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from .forms import NewBlogPost


@main.route('/')
def index():
    blogposts = BlogPost.query.all()
    return render_template('index.html', blogposts=blogposts)


@main.route('/add', methods=["GET", "POST"])
@login_required
def add_blogpost():
    form = NewBlogPost()
    # Submission handling
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        image = form.cover_image.data
        content = form.content.data

        new_blogpost = BlogPost(author=author, title=title, cover_image=image, content=content)
        db.session.add(new_blogpost)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add-pitch.html', form=form)
