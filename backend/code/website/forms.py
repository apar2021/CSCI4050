from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, Optional

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    phone = IntegerField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, message="Password must be at least 5 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email("This input requires a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetPasswordEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Reset Password')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Optional()])

    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    zipcode = IntegerField('Zip Code')  # Make sure to match the field name with your User model

    card_type = StringField('Card Type')
    card_number = IntegerField('Credit Card Number')
    expiration_date = StringField('Expiration Date')
    security_code = PasswordField('Security Code')

    submit = SubmitField('Save Changes')
    