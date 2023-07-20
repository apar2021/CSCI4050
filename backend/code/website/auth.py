from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm, ResetPasswordEmailForm, ResetPasswordForm
from .models import User
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from flask_mail import Message
import datetime

auth = Blueprint('auth', __name__)


@login_required
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            # Login successful, use Flask-Login to log the user in
            login_user(user)

            flash('Login successful!', 'success')
            print('2')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            print('3')
    print('bruh1')
    return render_template('Login.html', form = form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in instead.', 'error')
            return redirect(url_for('auth.login'))  # Redirect to login page if user already exists
        
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('auth.signup'))

        # If the email is not already registered, create a new User instance
        new_user = User(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            password= generate_password_hash(form.password.data, 'sha256')
        )

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        print("test2")

        flash('Registration successful! You may proceed to the email verification page.', 'success')
        return redirect(url_for('auth.email_verification'))

    print("test1")
    print(form.errors)
    return render_template('Registration.html', form = form)

@auth.route('/email-verification')
def email_verification():
    return render_template('RegistrationEmailVerification.html')


@auth.route('/logout')
def logout():
    return redirect(url_for('views.home'))


@auth.route('/edit-profile')
def edit_profile():
    return render_template('EditProfile.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password_email():
    form = ResetPasswordEmailForm()

    if form.validate_on_submit():
        # Process the form data here
        email = form.email.data
        # You can send an email to the user's email address with a reset link
        # For example:
        # send_reset_password_email(email) 

        user = User.query.filter_by(email=email).first()
        
        if user:
            token = secrets.token_urlsafe(16)  # Generate a token with 16 bytes (128 bits)

            # Save the token in the database associated with the user's email
            # This step is omitted in this example, and you should implement it in your code.
            # For example, you can have a column in the user's table to store the reset token.

            user.reset_token = token
            user.reset_token_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Set expiration to one hour from now
            db.session.commit()

            # Create the reset password email message
            msg = Message('Password Reset Request', sender='your_gmail_username', recipients=[email])
            # Set the content of the email (you can use HTML templates for a better email layout)
            msg.body = f'Click the following link to reset your password: {url_for("auth.reset_password", token=token, _external=True)}'
            # Send the email
            mail.send(msg)
            
            return render_template('ResetPasswordCorrectEmail.html')
        else: 
            return render_template('RegistrationIncorrectInformation.html')

    
    return render_template('ResetPasswordEmail.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Here, you should implement logic to verify the token
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash('Invalid token. Please request a new password reset.', 'error')
        return redirect(url_for('auth.forgot_password_email'))

    # You can also check if the token has expired and handle it accordingly
    # For example, if user.reset_token_expiration < datetime.utcnow():
    #     flash('Token has expired. Please request a new password reset.', 'error')
    #     return redirect(url_for('auth.forgot_password_email'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        print('work')
       
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('auth.reset_password', token=token))
       
        # Update the user's password with the new password
        user.password = generate_password_hash(form.password.data, 'sha256')

        # Clear the reset token from the user's account after successful password reset
        user.reset_token = None
        user.reset_token_expiration = None

        # Save the changes to the database
        db.session.commit()

        flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('ResetPassword.html', form=form)