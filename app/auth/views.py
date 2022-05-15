from flask import render_template, request, flash, redirect, url_for
from app import db
from . import auth
from .forms import LoginForm, SignupForm
from ..models import User
from flask_login import login_user, logout_user


@auth.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if login_form.validate_on_submit():

            email = login_form.email.data
            password = login_form.password.data

            get_user = User.query.filter_by(email=email).first()

            if get_user and User.verify_password(get_user, password):
                login_user(get_user)
                flash("Login successful", category="success")
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash("Wrong credentials", category="danger")
        else:
            flash("Please provide the necessary credentials below")

    return render_template('login.html', form=login_form)


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if request.method == "POST":
        if signup_form.validate_on_submit():
            check_existing = User.query.filter_by(email=signup_form.email.data).first()

            if check_existing is None:
                email = signup_form.email.data
                first_name = signup_form.first_name.data
                last_name = signup_form.last_name.data
                password = signup_form.password.data

                new_user = User(email=email, first_name=first_name, last_name=last_name, password=password, )

                # send_email("Welcome to PitchRank", "email/welcome_user", new_user.email, user=new_user)

                db.session.add(new_user)
                db.session.commit()

                flash("Signed up successfully", category="success")
                return redirect(url_for('auth.login'))
            else:
                flash("Email already registered. Please login", category="warning")
        else:
            flash("Please fill all fields with valid data", category="warning")
    return render_template('signup.html', form=signup_form)


@auth.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash('logged out successfully', category='danger')
    return redirect(url_for('auth.login'))
