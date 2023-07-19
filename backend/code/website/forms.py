from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from .models import User

class RegisterForm(FlaskForm):
    def validate_email_address(self,email_address_to_check):
        email = User.query.filter_by(email = email_address_to_check.data).first()
        if email:
            raise ValidationError('Email Address  already exists! Please try a different email address')

    name = StringField(label='Name',validators=[Length(min=5,max=100),DataRequired()])
    email = StringField(label = 'Email Address',validators=[Email(),DataRequired()])
    phone = IntegerField(label = 'Phone Number',validators=[Length(min=9,max=10), DataRequired()])
    password1 =  PasswordField(label='Password: ')
    password2 = PasswordField(label='Confirm Password: ',validators=[EqualTo('password1'),DataRequired()]) 
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label = 'Email Address',validators=[Email(),DataRequired()])
    password = PasswordField(label='Password: ',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class UserForm(FlaskForm):
    first_name = StringField(label='First Name :',validators=[DataRequired()])
    last_name  = StringField(label='Last Name :',validators=[DataRequired()])