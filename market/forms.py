from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from market.database import User


class Register(FlaskForm):
    def validate_username(self, username_check):
        user = User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError("User Name is already exists! Please change it to different value")

    def validate_email(self, email_check):
        email = User.query.filter_by(email=email_check.data).first()
        if email:
            raise ValidationError("Email is already exists! Please change it to different value")

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class Login(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItems(FlaskForm):
    submit = SubmitField(label="Purchase items")

class SellItems(FlaskForm):
    submit = SubmitField(label="Sell items")