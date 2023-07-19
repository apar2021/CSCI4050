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