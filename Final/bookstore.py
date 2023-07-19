from flask import Flask,render_template
app = Flask(__name__)

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

