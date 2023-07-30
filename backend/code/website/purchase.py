from flask import Blueprint, flash, redirect, url_for, session
from flask_login import current_user, login_required
from .models import Book, CartItem, Cart
from . import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/add_to_cart/<int:book_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(book_id, quantity=1):
    book = Book.query.get_or_404(book_id)
    
    if int(book.quantity) < int(quantity):
            flash(f'Not enough stock available for {book.name}.', 'error')
            return redirect(url_for('views.home'))
    
    # Get the session cart or create a new one if it doesn't exist
    cart = session.get('cart', {})

    # Add the book to the cart or update the quantity if it's already in the cart
    cart[str(book_id)] = cart.get(str(book_id), 0) + quantity

    session['cart'] = cart
    print(cart)

    flash('The book has been added to your cart.', 'success')
    return redirect(url_for('views.home'))


@purchase.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    return None

@purchase.route('/cart')
@login_required
def cart():
    return None
  
@purchase.route('/checkout', methods=['POST'])
@login_required
def checkout():
    return None

@purchase.route('/orders')
@login_required
def orders():
    return None