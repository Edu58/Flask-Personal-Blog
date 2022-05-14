from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class LoginForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    password = StringField('Your Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = StringField('Create a Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign up')
