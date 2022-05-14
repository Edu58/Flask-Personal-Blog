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


@main.route('/comment/<post_id>', methods=["GET", "POST"])
def add_comment(pitch_id):
    comment_form = CommentForm()

    pitch_comments = Pitches.query.filter_by(pitch_id=pitch_id).first()

    if request.method == "POST":
        if comment_form.validate_on_submit():

            comment = comment_form.comment.data
            new_comment = Comments(comment=comment, post_id=post_id, user_id=current_user.user_id)

            Comments.save_comment(new_comment)

            return redirect(url_for('main.index'))
        else:
            flash('Invalid comment. Remember, BE NICE')

    return render_template('comment.html', form=comment_form, comments=pitch_comments)
