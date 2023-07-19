from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    phone = IntegerField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')