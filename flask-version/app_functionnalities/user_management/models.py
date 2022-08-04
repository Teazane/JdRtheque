from App import database, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(64), nullable=False, index=True)
    password = database.Column(database.String(128), nullable=False)
    email = database.Column(database.String(256), nullable=False)
    playlists = database.relationship('Playlist', backref='user')

    def set_passwpord(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Méthode permettant de charger un utilisateur pour le login_manager
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))