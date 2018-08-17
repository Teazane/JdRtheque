# Gestionnaire de données (musiques, utilisateurs, etc.)
from models import User, Music
from App import database


class DataManager():

    def add_new_user(self, login, password, email):
        user = User(login=login, email=email)
        user.set_passwpord(password)
        database.session.add(user)
        database.commit()

    def add_new_musique(self, title, source, duration, loop):
        music = Music(title=title, source=source, duration=duration, loop=loop, vote=0)
        database.session.add(music)
        database.commit()
        # TODO:
        # style_tags = database.relationship('Style', secondary=music_style)
        # scene_tags = database.relationship('Scene', secondary=music_scene)

    def add_music_style_tag(self):
        # TODO
        return 0
    
    def add_music_scene_tag(self):
        # TODO
        return 0
