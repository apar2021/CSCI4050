from flask import Blueprint, render_template,request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash()
                logout_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash()
        else:
            flash()

    return render_template('Login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if(request.method == 'POST'):
         
        # required info
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')

        # address info (NOT required)
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        zipcode = request.form.get('zipcode')

        # payment info (NOT required)
        card_type = request.form.get('card_type')
        card_number = request.form.get('card_number')
        expiration_date = request.form.get('expiration_date')
        
        user = User.query.filter_by(email = email).first()
        
        if user:
            flash()

        # required info
        elif len(''):
            flash()
        elif len(''):
            flash()
    #    elif len(email) < 4:
    #        flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        
        # address info
        elif len(''):
            flash()
        elif len(''):
            flash()
        elif len(''):
            flash()
        elif len(''):
            flash()
        elif len(''):
            flash()
        
        # payment info
        elif len(''):
            flash()
        elif len(''):
            flash()
        elif len(''):
            flash()
        
        # creating user
        else:
            new_user = User(name = name, phone = phone, email = email, 
                            password = generate_password_hash(password1, method='sha256'), 
                            street = street, city = city, state = state, country = country, zipcode = zipcode,
                            card_type = card_type, card_number = card_number, expiration_date = expiration_date)
            db.session.add(new_user)
            db.session.commit()
            logout_user(user, remember = True)
            
            flash()
            return redirect(url_for('views.home'))

        

    return render_template('registration.html', user = current_user)