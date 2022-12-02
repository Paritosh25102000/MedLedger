#from app import app
import datetime
import json
from flask import Flask
import requests
from flask import render_template, redirect, request
#app.run(debug=True, port=5000, use_reloader=False)
print("Hello1")
app = Flask(__name__)
print("Hello2")
@app.route('/')
def home():
    #return "Hello"
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)