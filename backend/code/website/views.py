from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('Home.html')


@views.route('/cart')
def cart():
    return render_template('Cart.html')


@views.route('/order-history')
def order_history():
    return render_template('OrderHistory.html')


