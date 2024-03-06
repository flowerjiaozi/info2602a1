from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

#UserPokemon Model------------------------------------------------------------------------------------------
#Must get_json():json
class UserPokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
  name = db.Column(db.String(120))

  def get_json(self):

    return {
        "id": self.id,
        "user_id": self.user_id,
        "pokemon_id": self.pokemon_id,
        "name": self.name,
    }

  

#User Model-------------------------------------------------------------------------------------------------
#Must Catch, Release, Rename Pokemon
#Set and Check Password
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  #Relationship between user pokemon and user
  user_poke = db.relationship('UserPokemon', backref='user', lazy=True, cascade="all, delete-orphan")

  def catch_pokemon(self, pokemon_id, name):
    pokemon = Pokemon.query.get(pokemon_id)
    if not pokemon:
      return False
    else:
      user_pokemon =UserPokemon(user_id = self.id, pokemon_id=pokemon_id, name=name)
      db.session.add(user_pokemon)
      db.session.commit()
      return user_pokemon

  def release_pokemon(self, pokemon_id, name):
    user = User.query.filter_by(username=username).first()
    if not user:
      return False
    pokemon = User.query.filter_by(username=username).first()


 # def rename_pokemon(self, pokemon_id,name):

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)   

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='scrypt')

  def check_password(self, password):
    return check_password_hash(self.password, password)


#Pokemon Model-----------------------------------------------------------------------------------------------
#Must get_json():json
class Pokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  attack = db.Column(db.Integer)
  defense = db.Column(db.Integer)
  hp = db.Column(db.Integer)
  height = db.Column(db.Integer)
  sp_attack = db.Column(db.Integer)
  sp_defense = db.Column(db.Integer)
  speed = db.Column(db.Integer)
  type1 = db.Column(db.String(120))
  type2 = db.Column(db.String(120))
  weight = db.Column(db.Integer)
  pokeTwo = db.relationship('UserPokemon', backref='pokemon', lazy=True)

  def get_json(self):
    return {
        "id": self.id,
        "name": self.name,
        "attack": self.attack,
        "defense": self.defense,
        "hp": self.hp,
        "height": self.height,
        "sp_attack": self.sp_attack,
        "sp_defense": self.sp_defense,
        "speed": self.speed,
        "type1": self.type1,
        "type2": self.type2,
        "weight": self.weight,
        "pokeTwo": self.pokeTwo,
    }