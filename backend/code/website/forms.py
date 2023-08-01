from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, DecimalField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL, EqualTo, Optional

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    phone = IntegerField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, message="Password must be at least 5 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    street = StringField('Street', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    zipcode = IntegerField('Zip Code', validators=[Optional()])  # Make sure to match the field name with your User model

    card_type = StringField('Card Type', validators=[Optional()])
    card_number = IntegerField('Credit Card Number', validators=[Optional()])
    expiration_date = StringField('Expiration Date', validators=[Optional()]) 
    security_code = PasswordField('Security Code', validators=[Optional()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
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

    street = StringField('Street', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    zipcode = IntegerField('Zip Code', validators=[Optional()])  # Make sure to match the field name with your User model

    card_type = StringField('Card Type', validators=[Optional()])
    card_number = IntegerField('Credit Card Number', validators=[Optional()])
    expiration_date = StringField('Expiration Date', validators=[Optional()]) 
    security_code = PasswordField('Security Code', validators=[Optional()])

    submit = SubmitField('Save Changes')

class AddBookForm(FlaskForm):
    isbn = IntegerField('ISBN:', validators=[DataRequired()])
    category = StringField('Category:', validators=[DataRequired()])
    author = StringField("Authors' Names:", validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    image_url = StringField('Image URL:', validators=[DataRequired(), URL()])
    edition = StringField('Edition:', validators=[DataRequired()])
    publisher = StringField('Publisher:', validators=[DataRequired()])
    publication_year = IntegerField('Publication Year:', validators=[DataRequired()])
    quantity_in_stock = IntegerField('Quantity in Stock:', validators=[DataRequired()])
    minimum_threshold = IntegerField('Minimum Threshold:', validators=[DataRequired()])
    buying_price = DecimalField('Buying Price:', places=2, validators=[DataRequired()])
    selling_price = DecimalField('Selling Price:', places=2, validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class PromoCodeForm(FlaskForm):
    promo_code = StringField('Promo Code:', validators=[DataRequired()])
    percentage = StringField('Percentage:', validators=[DataRequired()])
    start_date = DateField('Start Date:', format='%Y-%m-%d', validators=[DataRequired()])
    expiration_date = DateField('Expiration Date:', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    promo_code = StringField('Promo Code:', validators=[Optional()])
    card_number = StringField('Card Number:', validators=[DataRequired()])
    expiration_date_m = StringField('Expiration Date:', validators=[DataRequired()])
    expiration_date_Y = StringField('Expiration Date:', validators=[DataRequired()])
    security_code = StringField('Security Code:', validators=[DataRequired()])
    save_card = BooleanField('Remember Card', validators=[Optional()])
    submit = SubmitField('Submit')