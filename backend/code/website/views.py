from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Book, Order, Cart, CartItem, Book
import random
from .forms import PaymentForm
views = Blueprint('views', __name__)

# Home page
@views.route('/')
@views.route('/home')
def home():
    random.seed(42)
    # Fetch all books from the database
    all_books = Book.query.all()
    # Select a random subset of books to display on the front page
    # Change the number (e.g., 4) to the desired number of random books you want to display
    if len(all_books) > 4:
        random_books = random.sample(all_books, 4)
    else:
        random_books = all_books

    # Get the 4 most recent books added to the database, reverse the list
    new_books = all_books[::-1][:4]

    # Pass the random_books to the front page (home.html) template
    return render_template('home.html', featured_books=random_books, new_books=new_books)

# Cart page
@views.route('/cart')
@login_required
def cart():
    # Get the session cart or create a new one if it doesn't exist
    cart = session.get('cart', {})
    books = []
    quantities = []
    for book_id, quantity in zip(cart.keys(), cart.values()):
        book = Book.query.get_or_404(book_id)
        books.append(book)
        quantities.append(quantity)

    return render_template('Cart.html', books=books, quantities=quantities, zip=zip)


# Checkout page
@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = PaymentForm()
    cart = session.get('cart', {})
    books = []
    quantities = []
    total = 0.0
    for book_id, quantity in zip(cart.keys(), cart.values()):
        book = Book.query.get_or_404(book_id)
        books.append(book)
        quantities.append(quantity)
        total += book.selling_price * quantity
    session["total"] = total


    if form.validate_on_submit():
        session["promo_code"] = form.promo_code.data
        session["card_number"] = form.card_number.data
        session["expiration_date"] = form.expiration_date_m.data + "/" + form.expiration_date_Y.data
        session["security_code"] = form.security_code.data
        session["save_card"] = form.save_card.data
        return redirect(url_for('purchase.checkout_cart'))
    else:
        # Outputting Errors
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')
    return render_template('Checkout.html', books=books, quantities=quantities, zip=zip, total=total, form=form)

# Product page
@views.route('/product/<int:book_id>')
def product(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('Product.html', book=book)


# Order History page
@views.route('/order-history')
@login_required
def order_history():
    # Get current user id
    user_id = current_user.id
    # Get all orders for the current user
    orders = Order.query.filter_by(userid=user_id).all()
    print(len(orders))
    # Get all the old carts for the current user
    carts = Cart.query.filter_by(userid=user_id).all()
    print(len(carts))
    # Get all the cart items for the old carts
    cart_items = []
    book_carts = []
    for cart in carts:
        print(cart)
        items = CartItem.query.filter_by(cartid=cart.id).all()
        books = []
        for item in items:
            books.append(Book.query.get(item.bookid))
        print(items)
        print(books)
        cart_items.append(items)
        book_carts.append(books)

    return render_template('OrderHistory.html', orders=orders, cart_items=cart_items, book_carts=book_carts, zip=zip)

# Admin Panel
@views.route('/admin-page')
def admin_page():
    return render_template('AdminPage.html')