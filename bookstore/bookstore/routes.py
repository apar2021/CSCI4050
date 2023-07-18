from . import app
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
from models import Item, User, Book
from forms import RegisterForm,LoginForm,UserForm
from bookstore import db
from flask_login import login_user,logout_user,login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=Book)


@app.route('/register')
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market.page'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}')
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are invalid! Please try again.',category='danger')


    return render_template('login.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!",category='Info')
    return redirect(url_for('home_page'))


@app.route('/update/<int:id>',methods=['GET','POST'])
def update_profile(id):
    form = UserForm()
    update_user = User.query.get_or_404(id)
    if request.method =="POST":
        update_user.first_name= request.form['']

""" 
@app.route('/reset-password')
def reset_password():
     """