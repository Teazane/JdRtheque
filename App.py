from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ----------------- Routing

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=False)


@app.route('/favico.ico')
def favicon():
    return ''


app.run(debug=True)

# ----------------- Tuto et liens utiles
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# http://jinja.pocoo.org/docs/2.10/templates/
