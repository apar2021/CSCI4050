from . import db
from flask_login import UserMixin

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
    
    #payment info
    card_type = db.Column(db.String(150))
    card_number = db.Column(db.Integer)
    expiration_date = db.Column(db.String(150))

    #reset password info

    reset_token = db.Column(db.String(100), unique=True)  # Store the reset token
    reset_token_expiration = db.Column(db.DateTime) 


    def __init__(self, name, phone, email, password, 
                 street="", city="", state="", country="", zipcode=None, card_type="", card_number=None, expiration_date="",
                 reset_token = None, reset_token_expiration = None):
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
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.reset_token = reset_token
        self.reset_token_expiration = reset_token_expiration

