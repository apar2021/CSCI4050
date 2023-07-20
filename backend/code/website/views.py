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

@views.route('/editaccount', methods=['GET', 'POST'])
@login_required
def editaccount():
    form = EditAccountForm()
    if request.method == 'POST':
        print('check data and submit')
    else:
        print('get data from db and add to form')


