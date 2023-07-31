from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .forms import RegistrationForm, LoginForm, ResetPasswordEmailForm, ResetPasswordForm, EditProfileForm
from .models import User, Cart
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from flask_mail import Message
import datetime
from cryptography.fernet import Fernet


auth = Blueprint('auth', __name__)

# Method to verify user login information
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Check if form is valid
    if form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        # Check if the password is correct
        if user and check_password_hash(user.password, form.password.data):
            # If if the user's email is verified
            if user.is_verified:
                if user.is_admin:
                    login_user(user)
                    flash('Login successful!', 'success')
                    return redirect(url_for('views.admin_page'))
                login_user(user)
                session["cart"] = {}
                flash('Login successful!', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Account Not Verified. Please Verify Account.', 'error')
        else:
            flash('Invalid email or password. Please try again.', 'error')
    else:
        # Outputting Errors
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')

    return render_template('Login.html', form = form)

# Method to verify a user's registration information and create a new user
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    # Check if form is valid
    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in instead.', 'error')
            return redirect(url_for('auth.login'))  # Redirect to login page if user already exists
        # Check if the password and confirm password fields match
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

        # Record email for verification
        email = form.email.data
        new_user.generate_verification_token()

        token = new_user.verification_token

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Send the verification email
        msg = Message('Account Verification', sender='your_gmail_username', recipients=[email])
        msg.body = f'Click the following link to verify your account: {url_for("auth.verify_account", token=token, _external=True)}'
        mail.send(msg)

        flash('Registration successful! You may proceed to the email verification page.', 'success')
        return redirect(url_for('auth.email_verification'))
    else:
        # Outputting Errors
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')

    return render_template('Registration.html', form = form)

# Method to update a user's verification status
@auth.route('/verify-account/<token>')
def verify_account(token):
    # Query for user data
    user = User.query.filter_by(verification_token=token).first()

    # Check if the user exists and if the token is valid
    if not user or user.verification_token_expiration < datetime.datetime.utcnow():
        flash('Invalid or expired verification token.', 'error')
        return redirect(url_for('auth.login'))

    # Update the database to verify the user's account
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expiration = None
    db.session.commit()

    flash('Your account has been verified successfully. You can now log in.', 'success')
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Method to redirect user view to confirm email confirmation
@auth.route('/email-verification')
def email_verification():
    return render_template('RegistrationEmailVerification.html')

# Method to log out a user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect the user to the desired page (e.g., home page or login page)
    return redirect(url_for('views.home'))

# Method to send a forgot password email
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password_email():
    form = ResetPasswordEmailForm()
    # Check if the form is valid
    if form.validate_on_submit():
        # Process the form data
        email = form.email.data
        # Find the user's account in the database via email
        user = User.query.filter_by(email=email).first()
        
        # If the user exists, generate a reset token and send the reset password email
        if user:
            token = secrets.token_urlsafe(16)  # Generate a token with 16 bytes (128 bits)
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
            return render_template('ResetPasswordIncorrectEmail.html')

    return render_template('ResetPasswordEmail.html', form=form)

# Method to reset a user's password
@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if the reset token is associated with a user account
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        flash('Invalid token. Please request a new password reset.', 'error')
        return redirect(url_for('auth.forgot_password_email'))

    form = ResetPasswordForm()
    # Validate Password Reset Data
    if form.validate_on_submit():
       # Check if the password and confirm password fields match
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

        # Confirm password reset to user
        flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
        return redirect(url_for('auth.login'))
    else:
        # Outputting Errors
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')

    return render_template('ResetPassword.html', form=form, token = token)

# Method to edit a user's profile
@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    # Load the current user's information into the form fields
    if request.method == 'GET':
        form.name.data = current_user.name
        form.phone.data = current_user.phone

        form.street.data = current_user.street
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zipcode.data = current_user.zipcode

        form.card_type.data = current_user.card_type
        form.card_number.data = current_user.decrypt_card_number()
        form.expiration_date.data = current_user.expiration_date
        form.security_code.data = current_user.decrypt_security_code()
    # Validate the form data
    if form.validate_on_submit():
        # Save the changes to the user's profile
        user = User.query.get(current_user.id)
        user.name = form.name.data
        user.phone = form.phone.data

        user.street = form.street.data
        user.city = form.city.data
        user.state = form.state.data
        user.zipcode = form.zipcode.data

        # Encrypt the card number and security code
        user.card_type = form.card_type.data
        if form.card_number.data:
            user.card_number_encrypted = user.encrypt(str(form.card_number.data))
        user.expiration_date = form.expiration_date.data

        if form.security_code.data:
            user.security_code_encrypted = user.encrypt(str(form.security_code.data))

        if form.password.data:
            user.password = generate_password_hash(form.password.data, 'sha256')
        
        db.session.commit()

        # Send a confirmation email to the user
        msg = Message('Profile Updated', sender='your_gmail_username', recipients=[current_user.email])
        msg.body = 'Your profile has been updated successfully.'
        mail.send(msg)

        # Confirm profile update to user
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('auth.edit_profile'))
    else:
        # Outputting Errors
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')
        return render_template('EditProfile.html', form=form)

# #way to search given criteria - not an advisable option in this case
# @auth.route('/search')
# def search():
#     query=request.args.get('query')
#     criteria=request.args.get('criteria')
#     if criteria=="title":
#         books=Book.query.filter(Book.title.
# @auth.route('/search')
# def search():
                                
            
