from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Book, CartItem, Cart
from . import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/add_to_cart/<int:book_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(book_id, quantity=1):
    book = Book.query.get_or_404(book_id)
    
    # Check if the user already has a cart, if not, create one
    if not current_user.cart:
        cart = Cart(userid=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # Find the user's cart and add the book to it
    cart = current_user.cart
    cart_item = CartItem(cartid=cart.id, bookid=book.id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

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