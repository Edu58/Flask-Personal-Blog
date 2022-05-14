from . import main
from app import db, photos
from app.models import BlogPost
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from .forms import NewBlogPost
from werkzeug.utils import secure_filename


@main.route('/')
def index():
    blogposts = BlogPost.query.all()
    return render_template('index.html', blogposts=blogposts)


@main.route('/<post_title>/<post_id>')
def read_post(post_title, post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    return render_template('single-post.html', post=post)


@main.route('/add/<user_id>', methods=["GET", "POST"])
@login_required
def add_blogpost(user_id):
    form = NewBlogPost()
    # Submission handling
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        image = form.cover_image.data
        content = form.content.data

        filename = secure_filename(image.filename)
        photos.save(image)
        path = f'photos/{filename}'
        new_blogpost = BlogPost(author=author, title=title, cover_image=path, content=content)
        db.session.add(new_blogpost)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add-blogpost.html', form=form)
