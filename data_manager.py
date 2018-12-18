# Gestionnaire de données (musiques, utilisateurs, etc.)
from models import User, Music, Scene, Style
from App import database


class DataManager:

    def add_new_user(self, login, password, email):
        user = User()
        user.login = login
        user.email = email
        user.set_passwpord(password)
        database.session.add(user)
        database.session.commit()

    def add_new_musique(self, title, source, duration, loop):
        music = Music(title=title, source=source, duration=duration, loop=loop, vote=0)
        database.session.add(music)
        database.session.commit()
        # TODO:
        # style_tags = database.relationship('Style', secondary=music_style)
        # scene_tags = database.relationship('Scene', secondary=music_scene)

    def add_music_style_tag(self, name):
        style = Style(name=name)
        database.session.add(style)
        database.session.commit()
    
    def add_music_scene_tag(self, name):
        scene = Scene(name=name)
        database.session.add(scene)
        database.session.commit()
