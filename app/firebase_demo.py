from pyrebase import pyrebase

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

def signup():
    email=input("Enter email: ")
    password=input("Enter password: ")
    user=auth.create_user_with_email_and_password(email,password)

signup()