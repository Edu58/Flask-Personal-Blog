from . import main
from app import db, photos
from app.models import BlogPost, Comments
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import NewBlogPost, CommentForm
from werkzeug.utils import secure_filename


@main.route('/')
def index():
    blogposts = BlogPost.query.all()
    return render_template('index.html', blogposts=blogposts)


@main.route('/<post_title>/<post_id>', methods=['GET', 'POST'])
def read_post(post_title, post_id):
    post = BlogPost.query.filter_by(post_id=post_id).first()

    comment_form = CommentForm()

    post_comments = Comments.query.filter_by(post_id=post_id).all()

    if request.method == "POST":
        if comment_form.validate_on_submit():

            comment = comment_form.comment.data
            username = comment_form.username.data
            new_comment = Comments(comment=comment, post_id=post_id, username=username)

            Comments.save_comment(new_comment)

            return redirect(url_for('main.read_post', post_id=post_id, post_title=post_title, comments=post_comments))
        else:
            flash('Invalid comment. Remember, BE NICE')

    return render_template('single-post.html', post=post, comment_form=comment_form, comments=post_comments)


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
