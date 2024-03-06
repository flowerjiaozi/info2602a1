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
@app.cli.command("init", help="Creates and initializes the database")
def initialize_db():
  db.drop_all()
  db.create_all()

  with open('pokemon.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      new_pokemon = Pokemon(text=row['text'])  #create object
      #update fields based on records
      #new_todo.done = True if row['done'] == 'true' else False
      new_pokemon.id = int(row['pokedex_number'])
      new_pokemon.name = str(row['name'])
      new_pokemon.attack = int(row['attack'])
      new_pokemon.defense = int(row['defense'])
      new_pokemon.hp = int(row['hp'])
      new_pokemon.weight = int(row['weight_kg'])
      new_pokemon.height = int(row['height_m'])
      new_pokemon.sp_attack = int(row['sp_attack'])
      new_pokemon.sp_defense = int(row['sp_defense'])
      new_pokemon.speed = int(row['speed'])
      new_pokemon.type1 = str(row['type1'])
      new_pokemon.type2 = str(row['type2']) if not row['type2'] else null
      

      db.session.add(new_pokemon)  #queue changes for saving
    db.session.commit()
    #save all changes OUTSIDE the loop
  print('database intialized')

# ********** Routes **************
@app.route('/')
def index():
  return '<h1>Poke API v1.0</h1>'

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)


#Faith Routes-------------------------------------------------------


#-------------------------------------------------------------------

