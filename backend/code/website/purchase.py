from flask import Blueprint, flash, redirect, url_for, session
from flask_login import current_user, login_required
from flask_mail import Message
from .models import Book, CartItem, Cart, Order, User
from . import db, mail
from datetime import datetime

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


@purchase.route('/remove_from_cart/<int:book_id>', methods=['POST'])
@login_required
def remove_from_cart(book_id):
    cart = session.get('cart', {})
    book_id = str(book_id)
    if book_id in cart:
        del cart[book_id]
        session['cart'] = cart
        flash('The book has been removed from your cart.', 'success')
    return redirect(url_for('views.cart'))
  
@purchase.route('/checkout_cart', methods=['GET', 'POST'])
@login_required
def checkout_cart():
    cart_session = session.get('cart', {})
    total = session.get('total', 0.00)
    if len(cart_session) == 0:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('views.home'))
    
    # Create a cart instance to store from session data
    cart = Cart(current_user.id)
    db.session.add(cart)
    db.session.commit()

    # Update Book Quantities
    for book_id, quantity in zip(cart_session.keys(), cart_session.values()):
        book = Book.query.get_or_404(book_id)
        if book.quantity < quantity:
            flash(f'Not enough stock available for {book.title}.', 'error')
            return redirect(url_for('views.home'))
        book.quantity -= quantity
        # Create a cart item for each book in the cart
        cart_item = CartItem(cartid=cart.id, bookid=book_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
    
    # Get current user
    user = User.query.get(current_user.id)

    if session.get('save_card', False):
        user.card_number_encrypted = user.encrypt(str(session.get('card_number', None)))
        user.expiration_date = session.get('expiration_date', None)
        user.security_code_encrypted = user.encrypt(str(session.get('security_code', None)))
        db.session.commit()
    
    
    


    # Create an order instance for the cart
    order = Order(userid=current_user.id, cartid=cart.id, card_number=session.get("card_number"), total_price=total, promotionid=None, order_date=datetime.now())
    # Encrypt the card number and security code
    if session.get('card_number', None):
        order.card_number = user.encrypt(str(session.get("card_number")))

    db.session.add(order)
    db.session.commit()
    # Clear the session variables
    session['cart'] = {}
    session['total'] = 0.00
    session['card_number'] = None
    session['expiration_date'] = None
    session['security_code'] = None
    session['save_card'] = False

    # Generate a confirmation code
    # Send the verification email
    msg = Message('Account Verification', sender='your_gmail_username', recipients=[current_user.email])
    msg.body = f'You Ordered!'
    mail.send(msg)

    return redirect(url_for('views.home'))

@purchase.route('/orders')
@login_required
def orders():
    return None