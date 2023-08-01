from flask import Blueprint, render_template, request
from .models import Book

search = Blueprint('search', __name__)

@search.route('/search', methods = ['GET'] )
def lookup():
    query = request.args.get('query')
    criteria = request.args.get('criteria')

    # Perform search based on the chosen criteria
    if criteria == 'title':
        books = Book.query.filter(Book.title.ilike(f"%{query}%")).all()
    elif criteria == 'author':
        books = Book.query.filter(Book.author.ilike(f"%{query}%")).all()
    elif criteria == 'category':
        books = Book.query.filter(Book.category.ilike(f"%{query}%")).all()
    elif criteria == 'ISBN':
        books = Book.query.filter(Book.isbn == query).all()
    else:
        # Handle other search criteria if needed
        books = []

    #print(books[0].title)
    return render_template('SearchView.html', books=books)
