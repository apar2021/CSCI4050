from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('Login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in instead.', 'error')
            return redirect(url_for('auth.login'))  # Redirect to login page if user already exists

        # If the email is not already registered, create a new User instance
        new_user = User(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
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

