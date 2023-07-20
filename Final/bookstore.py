from flask import Flask,render_template
from flask import UserMixin
app = Flask(__name__)

class User(db.Model,UserMixin):
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
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
if __name__=="__main__":
    app.run(debug=True)

