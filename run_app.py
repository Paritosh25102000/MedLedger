from app import app
import datetime
import json
from flask import Flask, request
from flask import render_template, redirect, request, flash
import requests
from pyrebase import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

firebaseConfig={'apiKey': "AIzaSyC83vQ38mfDiLDE7c1MN3-HU2D5BHNhSYE",
  'authDomain': "ehrblockchain-5c46d.firebaseapp.com",
  'projectId': "ehrblockchain-5c46d",
  'storageBucket': "ehrblockchain-5c46d.appspot.com",
  'messagingSenderId': "906741909883",
  'appId': "1:906741909883:web:0df1ee8afb765c8e5215de",
  'measurementId': "G-91LKP31BJF",
  'databaseURL': 'https://ehrblockchain-5c46d-default-rtdb.firebaseio.com'}

firebase= pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

cred = credentials.Certificate("ehrblockchain-5c46d-firebase-adminsdk-d3hq9-d1115a78a7.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

#app.run(debug=True, port=5000, use_reloader=False)


app = Flask(__name__)
app.secret_key= 'secret'
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

@app.route('/', methods=['GET', 'POST'])
def home():
    #return "Hello"
    return render_template('home.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=''
    if request.method=='POST' : 
        email=request.form.get('email')
        pasw=request.form.get('pasw')
        print(email)
        print(pasw)
        try:
            user=auth.sign_in_with_email_and_password(email,pasw)
            flash('Successfully logged in')
            return render_template('dashboard.html')
        except Exception as e:
            error= 'Invalid email or password. Please try again!'
            return render_template('login1.html', error=error)
        #   return "Invalid email or password"
        #   session_id = user['idToken']
        #   request.session['uid'] = str(session_id)  
    
    return render_template('login1.html', error=error)

    #             return redirect('/home')
    
    # return render_template('login1.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
            print('Reached Here')       
            email=request.form.get('email')
            pasw=request.form.get('pasw')
            try:
                user=auth.create_user_with_email_and_password(email,pasw)
                flash("Account created successfully")
            except:
                return "Email already exists"  
    return render_template('register.html')

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

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

@app.route('/home', methods=['GET', 'POST'])
def index():
    fetch_posts()
    return render_template('index1.html',
                           title='MedLedger',
                           body="A comprehensive Blockchain Repository for all your Health Records",
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    
    # role = request.form["role"]
    import sqlite3 as sql

    amount = request.form["amount"]
    post_content = request.form["content"]
    to=request.form["to"]
    need=request.form["need"]
    payment=request.form["payment"]

    post_object = {
        # 'role' : role,
        'amount' : amount,
        'content': post_content,
        'to': to,
        'need': need,
        'payment': payment,
        'time': str(time.strftime('%Y-%m-%d %H:%M:%S'))
    }
    d=[post_object]

    for record in d:
        doc_ref = db.collection(u'user_data').document(record['time'])
        doc_ref.set(record)
        # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    return redirect('/home')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')

@app.route('/display', methods=['GET', 'POST'])
def disp():
    users_ref=db.collection(u"user_data")
    docs= users_ref.stream()
    tab = []
    for doc in docs:
        res = doc.to_dict()
        l = []
        for key, values in res.items():
            l.append(values)
        tab.append(l)
    # final = '<br>'.join(tab)
    # return final
    return render_template('display.html', tab=tab)
        # return render_template('display.html')
        # return redirect("https://console.firebase.google.com/u/0/project/ehrblockchain-5c46d/firestore/data")

if __name__ == '__main__':
    app.run(debug=True, port=8000)