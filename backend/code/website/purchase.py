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
    print(1)
    cart = session.get('cart', {})
    print(cart)

    # Add the book to the cart or update the quantity if it's already in the cart
    print(2)
    print(cart.get(book_id, 0))
    cart[str(book_id)] = cart.get(str(book_id), 0) + quantity

    session['cart'] = cart
    print(3)
    print(cart)

    # Check if the user already has a cart, if not, create one
    #if not current_user.cart:
    #    cart = Cart(userid=current_user.id)
    #    db.session.add(cart)
    #    db.session.commit()

    # Find the user's cart and add the book to it
    #cart = current_user.cart
    #cart_item = CartItem(cartid=cart.id, bookid=book.id, quantity=quantity)
    #db.session.add(cart_item)
    #db.session.commit()
    #session["cart"] = {}
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