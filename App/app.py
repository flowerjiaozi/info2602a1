import os, csv
from flask import Flask, jsonify, request
from functools import wraps
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from .models import db, User, UserPokemon, Pokemon

# Configure Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySecretKey'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JWT_HEADER_TYPE'] = ""
app.config['JWT_HEADER_NAME'] = "Cookie"


# Initialize App 
db.init_app(app)
app.app_context().push()
CORS(app)
jwt = JWTManager(app)

# Initializer Function to be used in both init command and /init route
def initialize_db():
  db.drop_all()
  db.create_all()

# ********** Routes **************
@app.route('/')
def index():
  return '<h1>Poke API v1.0</h1>'

#Faith Routes-------------------------------------------------------
@app.cli.command('create-user')

@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')

def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    print("Username or email already taken!") #give the user a useful message
  else:
    print(newuser) # print the newly created user

#-------------------------------------------------------------------
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

