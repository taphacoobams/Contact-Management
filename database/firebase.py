import firebase_admin
 
from firebase_admin import credentials
 
import pyrebase
 
from configs.my_api_config import firebaseConfig
 
if not firebase_admin._apps:

    cred = credentials.Certificate("configs/key_config.json")
 
    firebase_admin.initialize_app(cred)
 
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
authContact = firebase.auth()