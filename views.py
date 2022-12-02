import datetime
import json
from flask import Flask
import requests
from flask import render_template, redirect, request
# from app import app
# import os
# import pyrebase

# firebaseConfig={'apiKey': "AIzaSyC83vQ38mfDiLDE7c1MN3-HU2D5BHNhSYE",
#   'authDomain': "ehrblockchain-5c46d.firebaseapp.com",
#   'projectId': "ehrblockchain-5c46d",
#   'storageBucket': "ehrblockchain-5c46d.appspot.com",
#   'messagingSenderId': "906741909883",
#   'appId': "1:906741909883:web:0df1ee8afb765c8e5215de",
#   'measurementId': "G-91LKP31BJF"}

# firebase= pyrebase.initialize_app(firebaseConfig)
# auth=firebase.auth()

# def signup():
#     email=input("Enter email: ")
#     password=input("Enter password: ")
#     user=auth.create_user_with_email_and_password(email,password)
    

app=Flask(__name__)
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:5000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/home')
def index():
    fetch_posts()
    return render_template('index1.html',
                           title='EHR Blockchain',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    
    author = request.form["author"]
    role = request.form["role"]
    amount = request.form["amount"]
    email = request.form["email"]
    post_content = request.form["content"]

    post_object = {
        'author': author,
        'role' : role,
        'amount' : amount,
        'email' : email,
        'content': post_content
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

# from flask import Flask, render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db.sqlite3'
# app.config['SECRET_KEY'] = 'thisisasecretkey'
# app.config['SESSION_TYPE'] = 'filesystem' 
# app.config['SESSION_PERMANENT']= False 
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)



# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


# class RegisterForm(FlaskForm):
#     username = StringField(validators=[
#                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[
#                              InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Register')

#     def validate_username(self, username):
#          existing_user_username = User.query.filter_by(username=username.data).first()
#          if existing_user_username:
#              raise ValidationError(
#                  'That username already exists. Please choose a different one.')


# class LoginForm(FlaskForm):
#     username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

#     password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

#     submit = SubmitField('Login')

# @app.route('/')
# def home():
#     return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST' : 
        # email = request.form.get('email')
        # pasw = request.form.get('pass')
        # try:
        #     user = auth.create_user_with_email_and_password(email,password)
        #     print("Successfully created account")
        # except:
        #     return "Invalid credentials!"
        # session_id = user['idToken']
        # request.session['uid'] = str(session_id)
        pass
    return render_template(request, 'login1.html')


# @app.route('/dashboard', methods=['GET', 'POST'])
# # @login_required
# def dashboard():
#     return render_template('dashboard.html')


# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     # logout_user()
#     # return redirect(url_for('login'))
#     return "You have been logged out"


@app.route('/register', methods=['GET', 'POST'])
def register():
    return "working"
    # form = RegisterForm()
    # print(form)
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     new_user = User(username=form.username.data, password=hashed_password)
    #     db.session.add(new_user)
    #     # db.session.commit()
    #     return redirect('/login')

    # return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=8000, debug=True)