from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  login = db.Column(db.String, unique=True)
  password = db.Column(db.String, nullable=False)

class Notes(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  theme = db.Column(db.String)
  text = db.Column(db.String)
  user = db.Column(db.Integer)

# добавить поле для заметок