from bookstore import db, login_manager
from bookstore import Bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    first_name = db.Column(db.String(length=30),nullable=False)
    last_name = db.Column(db.String(length=30),nullable=False)
    password_hash = db.Column(db.Integer(),nullable=False,default=1000)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = Bcrypt.generate_password_hash(plain_text_password).decode('UTF-8')


class Item(db.Model):
    id  = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    isbn = db.Column(db.String(length=15),nullable=False,unique=True)
    description = db.Column(db.String(length=1024),nullable=False,unique=True)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item {self.name}'
