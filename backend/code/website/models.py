from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
from cryptography.fernet import Fernet

# Table containing user information
# Todo: Move payments into a separate table
# Todo: Move optional address info into separate table
# Waiting for eric for ^^^^ so I dont break stuff
class User(db.Model, UserMixin):
    __tablename__="users"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # user information
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    
    # user address
    street = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    country = db.Column(db.String(150))
    zipcode = db.Column(db.Integer)
    
    # payment info
    card_type = db.Column(db.String(150))
    card_number_encrypted  = db.Column(db.String(150))
    expiration_date = db.Column(db.String(150))
    security_code_encrypted  = db.Column(db.String(10))

    # verification
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), unique=True)
    verification_token_expiration = db.Column(db.DateTime)

    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe(32)
        self.verification_token_expiration = datetime.utcnow() + timedelta(hours=24)

    # reset password info
    reset_token = db.Column(db.String(100), unique=True)  # Store the reset token
    reset_token_expiration = db.Column(db.DateTime) 

    # admin
    is_admin = db.Column(db.Boolean, default=False)

    # encryptor attribute
    encryption_key = Fernet.generate_key()
    encryptor = Fernet(encryption_key)

    def __init__(self, name, phone, email, password, 
                 street="", city="", state="", country="", zipcode=None, 
                 card_type="", card_number=None, expiration_date="", security_code=None,
                 reset_token=None, reset_token_expiration=None, is_admin=False):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode
        self.card_type = card_type
        self.expiration_date = expiration_date
        self.reset_token = reset_token
        self.reset_token_expiration = reset_token_expiration
        self.is_admin = is_admin

        if card_number:
            self.card_number_encrypted = self.encrypt(str(card_number))
        else:
            self.card_number_encrypted = None

        if security_code:
            self.security_code_encrypted = self.encrypt(str(security_code))
        else:
            self.security_code_encrypted = None

    def encrypt(self, data):
        if data:
            return User.encryptor.encrypt(data.encode()).decode()
        return None

    def decrypt_card_number(self):
        if self.card_number_encrypted:
            return User.encryptor.decrypt(self.card_number_encrypted.encode()).decode()
        return None

    def decrypt_security_code(self):
        if self.security_code_encrypted:
            return User.encryptor.decrypt(self.security_code_encrypted.encode()).decode()
        return None

# Table containing Book Information
class Book(db.Model, UserMixin):
    __tablename__="books"

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    # book attributes
    isbn = db.Column(db.Integer)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    edition = db.Column(db.String(50))
    category = db.Column(db.String(100))
    publisher = db.Column(db.String(150))
    publication_year = db.Column(db.Integer)

    def __init__(self, isbn, title, author, edition, category, publisher, publication_year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.edition = edition
        self.category = category
        self.publisher = publisher
        self.publication_year = publication_year

# Table containing Inventory Information
class Inventory(db.Model, UserMixin):
    __tablename__="inventory"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(150))
    selling_price = db.Column(db.Float)
    buying_price = db.Column(db.Float)
    min_threshold = db.Column(db.Integer)

    def __init__(self, bookid, quantity, status, selling_price, buying_price, min_threshold):
        self.bookid = bookid
        self.quantity = quantity
        self.status = status
        self.selling_price = selling_price
        self.buying_price = buying_price
        self.min_threshold = min_threshold

# Table containing Promotion Information
class Promotion(db.Model, UserMixin):
    __tablename__="promotion"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    discount = db.Column(db.Float)
    promotion_start_date = db.Column(db.DateTime)
    promotion_end_date = db.Column(db.DateTime)

    def __init__(self, discount, promotion_start_date, promotion_end_date):
        self.discount = discount
        self.promotion_start_date = promotion_start_date
        self.promotion_end_date = promotion_end_date

# Table containing associations between users and carts
# Create a new cart entry for the user after every checkout
class Cart(db.Model, UserMixin):
    __tablename__="cart"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, userid):
        self.userid = userid

# Table containing associations between carts and book items
class CartItems(db.Model, UserMixin):
    __tablename__="cart_items"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    cartid = db.Column(db.Integer, db.ForeignKey('cart.id'))
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    quantity = db.Column(db.Integer)

    def __init__(self, cartid, bookid, quantity):
        self.cartid = cartid
        self.bookid = bookid
        self.quantity = quantity

# Table containing associations between carts and transactions
class Transaction(db.Model, UserMixin):
    __tablename__="transaction"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    cartid = db.Column(db.Integer, db.ForeignKey('cart.id'))

    # Number of times the order has been placed
    quantity = db.Column(db.Integer)  

    def __init__(self, cartid, quantity):
        self.cartid = cartid
        self.quantity = quantity

# Table containing information about past orders
class Order(db.Model, UserMixin):
    __tablename__="order"

    # primary key
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    transactionid = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    # Todo: Change to cardid
    card_number = db.Column(db.Integer, db.ForeignKey('users.card_number_encrypted'))
    #cardid = db.Column(db.Integer, db.ForeignKey('card.id'))
    # The total price is the price of the transaction times its quanitity
    total_price = db.Column(db.Float)
    promotionid = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    order_date = db.Column(db.DateTime)

    def __init__(self, userid, transactionid, cardid, total_price, promotionid, order_date):
        self.userid = userid
        self.transactionid = transactionid
        self.cardid = cardid
        self.total_price = total_price
        self.promotionid = promotionid
        self.order_date = order_date

# Todo: Add Card Table and move encryption from user into it


    
