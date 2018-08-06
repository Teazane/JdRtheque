from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)

import models

# ----------------- Routing

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=False)


@app.route('/favico.ico')
def favicon():
    return ''

# ----------------- Lancement de l'appli'

app.run(debug=True)

# ----------------- Tuto et liens utiles
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# http://jinja.pocoo.org/docs/2.10/templates/
