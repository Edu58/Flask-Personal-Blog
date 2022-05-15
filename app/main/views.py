from . import main
from app import db, photos
from app.models import BlogPost, Comments, User
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .forms import NewBlogPost, CommentForm
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from api_requests import get_quote


@main.route('/')
def index():
    blogposts = BlogPost.query.order_by(desc(BlogPost.created_on))

    quote = get_quote()
    return render_template('index.html', blogposts=blogposts, quote=quote)


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
        new_blogpost = BlogPost(author=author, title=title, cover_image=path, content=content,
                                user_id=current_user.user_id)
        db.session.add(new_blogpost)
        db.session.commit()

        flash('Post added successfully', category='success')

        return redirect(url_for('main.index'))

    return render_template('add-blogpost.html', form=form)


@main.route('/<post_id>', methods=["GET", "DELETE"])
@login_required
def delete_post(post_id):
    post_to_delete = BlogPost.query.filter_by(post_id=post_id).first()

    if post_to_delete:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post deleted successfully', category='success')
        return redirect(url_for('main.index'))
    else:
        pass

    return redirect(url_for('main.index'))


@main.route('/<post_title>/<post_id>/<comment_id>', methods=["GET", "DELETE"])
@login_required
def delete_comment(post_title, post_id, comment_id):
    comment_to_delete = Comments.query.filter_by(comment_id=comment_id).first()

    if comment_to_delete:
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash('Comment deleted successfully', category='success')
        return redirect(url_for('main.read_post', post_title=post_title, post_id=post_id))
    else:
        pass


@main.route('/profile/<first_name>', methods=["GET", "POST"])
@login_required
def profile(first_name):
    posts = BlogPost.query.filter_by(user_id=current_user.user_id).all()

    print(posts)

    return render_template('profile.html', user=current_user, posts=posts)


@main.route('/user/upload-profile-picture/<user_id>', methods=['POST'])
@login_required
def upload_profile_pic(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_path = path
        db.session.commit()

    return redirect(url_for('main.profile', first_name=current_user.first_name))


@main.route('/update-profile-picture/<user_id>', methods=['POST'])
@login_required
def update_profile_pic(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        abort(404)

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_path = path
        db.session.commit()

    return redirect(url_for('main.profile', first_name=current_user.first_name))


@main.route('/update-post/<post_id>', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    form = NewBlogPost()

    post = BlogPost.query.filter_by(post_id=post_id).first()

    if request.method == 'GET':
        form.author.data = post.author
        form.title.data = post.title
        form.content.data = post.content

    if post is None:
        abort(404)

    # Submission handling
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        image = form.cover_image.data
        content = form.content.data

        filename = secure_filename(image.filename)
        photos.save(image)
        path = f'photos/{filename}'
        post.title = title
        post.author = author
        post.cover_image = path
        post.content = content
        db.session.commit()

        flash('Post updated successfully', category='success')

        return redirect(url_for('main.index'))

    return render_template('update-post.html', post=post, form=form)
