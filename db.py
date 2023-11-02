import pyrebase
from datetime import datetime
import hashlib  # For password hashing
import json

firebaseConfig = {
  "apiKey": "AIzaSyBIa20ao3DoT4XTiG-hxlTtAu6l4HIVOSE",
  "authDomain": "visual-product-recogniti-d7cb0.firebaseapp.com",
  "databaseURL": "https://visual-product-recogniti-d7cb0-default-rtdb.firebaseio.com",
  "projectId": "visual-product-recogniti-d7cb0",
  "storageBucket": "visual-product-recogniti-d7cb0.appspot.com",
  "messagingSenderId": "732077642124",
  "appId": "1:732077642124:web:84fc3eeb016d277c4c46a9",
  "measurementId": "G-GK2TPTMQ23"
}

firebase=pyrebase.initialize_app(firebaseConfig)
pyrebase_db=firebase.database()

auth = firebase.auth()

db = firebase.database()

def CreateTransaction(accountNumber, transactionType, transactionAmount):
    # Get the current date and time
    current_datetime = datetime.now()
    transactionRecipient= current_datetime.strftime(f"%Y-%m-%d %H:%M:%S")
    
    transaction_data = {
        "type": transactionType,
        "amount": transactionAmount,
        "recipient": transactionRecipient
    }

    db.child("Account").child(accountNumber).child("transactions").push(transaction_data)


CreateTransaction(1, 2, 3)

