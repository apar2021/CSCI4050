from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required
from .models import Book
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
    form = PaymentForm()
    if form.validate_on_submit():
        # Outputting Errors
        
        for error, message in zip(form.errors.keys(), form.errors.values()):
            flash(f'{error.capitalize()} Error: {message[0]}')
    print("ALERT ALERT ALERT")
    return render_template('Checkout.html', books=books, quantities=quantities, zip=zip, total=total, form=form)

# Product page
@views.route('/product/<int:book_id>')
def product(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('Product.html', book=book)


# Order History page
@views.route('/order-history')
def order_history():
    return render_template('OrderHistory.html')

# Admin Panel
@views.route('/admin-page')
def admin_page():
    return render_template('AdminPage.html')