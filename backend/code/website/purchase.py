from flask import Blueprint, flash, redirect, url_for, render_template, request, session
from .models import Book, Promotion, Cart, CartItem, Order
#from .forms import AddBookForm, PromoCodeForm
from . import db

from flask_login import current_user, login_required

purchase = Blueprint('purchase', __name__)

@purchase.route('/add_to_cart/<int:book_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(book_id, quantity=1):
    # Check if the book exists
    book_id = request.form.get('book_id') # TEMPORARY
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('views.home'))
    
    # Check if there are enough books in stock
    if book.quantity < quantity:
        flash(f'Not enough stock available for {book.name}.', 'error')
        return redirect(url_for('views.home'))
    
    # Get the session cart or create a new one if it doesn't exist
    cart = session.get('cart', {})

    # Update local cart
    cart[book_id] = cart.get(book_id, 0) + quantity

    # Update Server Cart
    session['cart'] = cart

    # Output completion message
    flash(f'Book{"s" if quantity > 1 else ""} Added To Cart!', 'success')
    return redirect(url_for('views.home'))


@purchase.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    cart_id = int(request.form['cart_id'])
    quantity = int(request.form['quantity'])

    cart_item = Cart.query.get(cart_id)
    if not cart_item:
        flash('Item not found in cart.', 'error')
    else:
        if cart_item.quantity <= quantity:
            db.session.delete(cart_item)
        else:
            cart_item.quantity -= quantity

        db.session.commit()
        flash('Item removed from cart.', 'success')

    return redirect(url_for('cart'))

@purchase.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_cost = 0

    for cart_item in cart_items:
        product = Book.query.get(cart_item.product_id)
        if not product:
            continue

        total_cost += product.price * cart_item.quantity

    return render_template('cart.html', cart_items=cart_items, total_cost=total_cost)
  
@purchase.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('home'))

    total_cost = 0
    for cart_item in cart_items:
        product = Book.query.get(cart_item.product_id)
        if not product:
            continue

        total_cost += product.price * cart_item.quantity

        # Check if the product quantity is sufficient for the order
        if product.quantity < cart_item.quantity:
            flash(f'Not enough stock available for {product.name}.', 'error')
            return redirect(url_for('cart'))

    # Create a new order
    order = Order(user_id=current_user.id, total_cost=total_cost)
    db.session.add(order)

    # Move cart items to order items and update the product quantity
    for cart_item in cart_items:
        product = Book.query.get(cart_item.product_id)
        if not product:
            continue

        order_item = Order(order_id=order.id, product_id=product.id, quantity=cart_item.quantity, price=product.price)
        db.session.add(order_item)

        product.quantity -= cart_item.quantity
        db.session.delete(cart_item)

    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('orders'))

@purchase.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=orders)