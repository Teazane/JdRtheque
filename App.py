from flask import Flask, render_template

app = Flask(__name__)

# ----------------- Routing

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', user=False)

@app.route('/favico.ico')
def favicon():
    return ''



# ----------------- Tuto et liens utiles
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# http://jinja.pocoo.org/docs/2.10/templates/
