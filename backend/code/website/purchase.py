from flask import Blueprint, flash, redirect, url_for, session, request
from flask_login import current_user, login_required
from flask_mail import Message
from .models import Book, CartItem, Cart, Order, User
from . import db, mail
from datetime import datetime
import secrets

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

@purchase.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    cart = session.get('cart', {})
    
    for book_id, quantity in cart.items():
        quantity_key = f'quantity_{book_id}'
        new_quantity = request.form.get(quantity_key)
        
        if new_quantity is not None:
            new_quantity = int(new_quantity)
            # Get the book from the database
            book = Book.query.get_or_404(book_id)
            
            # Check if the requested quantity is available
            if new_quantity <= book.quantity:
                cart[book_id] = new_quantity
            else:
                flash(f"Sorry, there are only {book.quantity} copies available for '{book.title}'.", 'error')
    
    session['cart'] = cart
    flash('Cart updated successfully!', 'success')
    print(cart)
    return redirect(url_for('views.cart'))


@purchase.route('/remove_from_cart/<int:book_id>', methods=['POST'])
@login_required
def remove_from_cart(book_id):
    cart = session.get('cart', {})
    book_id = str(book_id)
    if book_id in cart:
        book = Book.query.get_or_404(book_id)
        del cart[book_id]
        session['cart'] = cart
        flash(f"The book '{book.title}' has been removed from your cart.", 'success')
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

    send_order_confirmation_email(cart, order)

    return redirect(url_for('views.home'))



def send_order_confirmation_email(cart, order):
    subject = 'Order Confirmation'
    sender = 'your_gmail_username'
    recipients = [current_user.email]

    confirmation_code = secrets.token_hex(4).upper() 

    # Create a formatted message body with order details
    msg_body = f"Dear {current_user.name},\n\nThank you for your order!\n\nOrder Details:\n"

    items = CartItem.query.filter_by(cartid=cart.id).all()

    for item in items:
        book = Book.query.get(item.bookid)
        msg_body += f"- {book.title} (Quantity: {item.quantity})\n"


    msg_body += f"\nTotal Price: ${order.total_price}\n\nIf you have any questions or concerns, please don't hesitate to contact us.\n\nBest regards,\nThe Bookstore Team"

    msg_body += f"Confirmation Code: {confirmation_code}\n\n"
    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = msg_body
    mail.send(msg)




@purchase.route('/orders')
@login_required
def orders():
    return None