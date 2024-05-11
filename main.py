from flask import Flask, render_template, redirect, request
from instance.DataBase import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user



app = Flask(__name__)
app.secret_key = '79d77d1e7f9348c59a384d4376a9e53f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db.init_app(app)
manager = LoginManager(app)
manager.init_app(app)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
  try:
    users = User.query.all()
  except:
     users = None
  return render_template('index.html', users=users)

#добавление удаление и просмотр заметок


@app.route('/all_notes')
def all_notes():
    notes = Notes.query.filter_by(user=current_user.id).all()
    return render_template('all_notes.html',notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add():
    if request.method=="GET":
      return render_template('add.html')
    theme = request.form.get('theme')
    text = request.form.get('text')
    try:
      new_note = Notes(theme=theme, text=text, user=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      return redirect('/')
    except:
       return 'error'

# регистрация и вход
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
      return render_template('sign-up.html')
    login = request.form.get('login')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password1!=password2:
      return render_template('sign-up.html')
    user = User.query.filter_by(login=login).first()
    if user is not None:
      return render_template('sign-up.html')
    try:
      password = generate_password_hash(password=password1)
      new_user = User(login=login, password=password)
      db.session.add(new_user)
      db.session.commit()
      return redirect('/')
    except:
      print(login)
      return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method=='GET':
    return render_template('login.html')
  login = request.form.get('login')
  password = request.form.get('password')
  user = User.query.filter_by(login=login).first()
  if user is None:
    return redirect('/')
  if check_password_hash(user.password, password):
     login_user(user)
     return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=8000, debug=True)