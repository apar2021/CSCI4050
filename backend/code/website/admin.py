from flask import Blueprint, flash, redirect, url_for, render_template
from .models import Book, Promotion
from .forms import AddBookForm, PromoCodeForm
from . import db

admin = Blueprint('admin', __name__)


@admin.route('/add-book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    
    if form.validate_on_submit():
        print(form.data)
        # Create a new Book instance and populate it with form data
        new_book = Book(
            isbn=form.isbn.data,
            category=form.category.data,
            author=form.author.data,
            title=form.title.data,
            image_url=form.image_url.data,
            edition=form.edition.data,
            publisher=form.publisher.data,
            publication_year=form.publication_year.data,
            quantity = form.quantity_in_stock.data,
            status= "Available",
            selling_price = form.selling_price.data,
            buying_price = form.buying_price.data,
            min_threshold = form.minimum_threshold.data
        )

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        flash('The book has been added successfully.', 'success')
        return redirect(url_for('admin.add_book'))
    
    print('1')
    print(form.errors)
    return render_template('AddBooks.html', form = form)


@admin.route('/add-promo', methods=['GET', 'POST'])
def add_promo():
    
    form = PromoCodeForm()

    if form.validate_on_submit():

        # Create a new PromoCode instance and populate it with form data
        new_promo = Promotion(
            promo_code = form.promo_code.data,
            percentage = form.percentage.data,
            start_date = form.start_date.data,
            expiration_date = form.expiration_date.data
        )

        # Add the new promo code to the database
        db.session.add(new_promo)
        db.session.commit()

        flash('The promo code has been added successfully.', 'success')
        return redirect(url_for('admin.add_promo'))
    
    return render_template('AddPromotions.html', form = form)