from App import database, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

music_scene = database.Table('music_scene',
                             database.Column('scene_id', database.Integer, database.ForeignKey('scene.id'), primary_key=True),
                             database.Column('music_id', database.Integer, database.ForeignKey('music.id'), primary_key=True)
                             )

music_style = database.Table('music_style',
                             database.Column('style_id', database.Integer, database.ForeignKey('style.id'), primary_key=True),
                             database.Column('music_id', database.Integer, database.ForeignKey('music.id'), primary_key=True)
                             )

playlist_music = database.Table('playlist_music',
                                database.Column('playlist_id', database.Integer, database.ForeignKey('playlist.id'), primary_key=True),
                                database.Column('music_id', database.Integer, database.ForeignKey('music.id'), primary_key=True)
                                )


class Music(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(150), nullable=False, index=True)
    source = database.Column(database.String(150), nullable=False)
    duration = database.Column(database.Integer, nullable=False)
    loop = database.Column(database.Boolean, nullable=False)
    vote = database.Column(database.Integer, nullable=False)
    style_tags = database.relationship('Style', secondary=music_style)
    scene_tags = database.relationship('Scene', secondary=music_scene)


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


class Style(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), nullable=False, index=True)


class Scene(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), nullable=False, index=True)


class Playlist(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(32), nullable=False)
    musics = database.relationship('Music', secondary=playlist_music)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
