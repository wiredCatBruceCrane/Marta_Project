from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

app = Flask('Marta Project')

# app = Flask(__name__)
CORS(app)