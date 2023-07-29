from flask import Blueprint, render_template
from flask_login import login_required
from .models import Book
import random
views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
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


@views.route('/cart')
@login_required
def cart():
    return render_template('Cart.html')


@views.route('/order-history')
def order_history():
    return render_template('OrderHistory.html')

@views.route('/admin-page')
def admin_page():
    return render_template('AdminPage.html')


