from flask import Flask, render_template, redirect, url_for, request
from werkzeug.urls import url_parse
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__)
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User
from webforms import LoginForm, RegisterForm
from data_manager import DataManager
data_manager = DataManager()

# ----------------- Routing
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Accueil')


@app.route('/favico.ico')
def favicon():
    return ''


@app.route('/connexion', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Si déjà connecté
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # Vérifie qu'on est dans le cas d'une requête POST et qu'on valide
        user = User.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):  # Si mauvais login ou mdp
            # TODO : Voir pour une message d'erreur
            return redirect(url_for('login'))
        # TODO : Voir pour un message de confirmation
        login_user(user)
        next_page = request.args.get('next')  # Récupération de la page de redirection s'il y en avait une
        if not next_page or url_parse(next_page).netloc != '':  # netloc doit être nul (empêche une redirection malicieuse vers un autre domaine)
            next_page = url_for('index')  # Sinon mettre "index" comme page de retour
        return redirect(next_page)
    else:
        return render_template('login.html', form=form, title='Connexion')


@app.route('/compte')
@login_required
def account():
    return render_template('account.html', user=False, title='Mon compte')


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:  # Si déjà connecté
        form = RegisterForm()
        if form.validate_on_submit():  # Vérifie qu'on est dans le cas d'une requête POST et qu'on valide
            data_manager.add_new_user(form.login.data, form.password.data, form.email.data)
            # TODO : Voir pour un message de confirmation
            return redirect(url_for('index'))
        return render_template('register.html', form=form, title='Inscription')
    else:
        return redirect(url_for('index'))


@app.route('/deconnexion')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/rechercher_musique')
def music_search():
    # TODO
    return render_template('music_search.html', title='Banque sonore')


# ----------------- Lancement de l'appli'

# app.run(debug=True)

# ----------------- Tuto et liens utiles
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# http://jinja.pocoo.org/docs/2.10/templates/
# https://dev.mysql.com/doc/refman/5.7/en/default-privileges.html
# https://dev.mysql.com/doc/refman/5.7/en/adding-users.html 
