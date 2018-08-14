from flask import Flask, render_template, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
login_manager = LoginManager(app)

import models
from webforms import LoginForm, RegisterForm
from data_manager import DataManager

# ----------------- Routing
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=False)


@app.route('/favico.ico')
def favicon():
    return ''


@app.route('/connexion', methods=['GET', 'POST'])
def login():
    # TODO : Vérifier qu'un utilisateur n'est pas déjà connecté
    form = LoginForm()
    if form.validate_on_submit():  # Vérifie qu'on est dans le cas d'une requête POST et qu'on valide
        return redirect(url_for('index'))
    return render_template('login.html', user=False, form=form)


@app.route('/compte')
def account():
    # TODO : Vérifier qu'un utilisateur est connecté
    return render_template('account.html', user=False)


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    # TODO : Vérifier qu'un utilisateur n'est pas déjà connecté
    form = RegisterForm()
    if form.validate_on_submit():  # Vérifie qu'on est dans le cas d'une requête POST et qu'on valide
        DataManager.add_new_user(form.login.data, form.password.data, form.email.data)
        return redirect(url_for('index'))  # TODO : décider de la page de redirection
    return render_template('register.html', user=False, form=form)


@app.route('/deconnexion')
def logout():
    # TODO : Vérifier qu'un utilisateur est déjà connecté
    return render_template('index.html', user=False)


@app.route('/rechercher_musique')
def music_search():
    # TODO
    return render_template('music_search.html', user=False)


# ----------------- Lancement de l'appli'

# app.run(debug=True)

# ----------------- Tuto et liens utiles
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# http://jinja.pocoo.org/docs/2.10/templates/
# https://dev.mysql.com/doc/refman/5.7/en/default-privileges.html
# https://dev.mysql.com/doc/refman/5.7/en/adding-users.html 
