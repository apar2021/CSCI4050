from flask import Blueprint, flash, redirect, url_for, render_template
from .models import Book
from .forms import AddBookForm
from . import db

admin = Blueprint('admin', __name__)


@admin.register('/add-book')
def add_book():
    form = AddBookForm()
    
    if form.validate_on_submit():
        # Create a new Book instance and populate it with form data
        new_book = Book(
            isbn=form.isbn.data,
            category=form.category.data,
            authors=form.authors.data,
            title=form.title.data,
            image_url=form.image_url.data,
            edition=form.edition.data,
            publisher=form.publisher.data,
            publication_year=form.publication_year.data,
            quantity_in_stock=form.quantity_in_stock.data,
            minimum_threshold=form.minimum_threshold.data,
            buying_price=form.buying_price.data,
            selling_price=form.selling_price.data
        )

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        flash('The book has been added successfully.', 'success')
        return redirect(url_for('admin.add_book'))

    return render_template('AddBooks.html')

@admin.register('/add-promo')
def add_promo():

    
    return render_template('AddPromotions.html')