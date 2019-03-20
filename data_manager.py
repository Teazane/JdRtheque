# Gestionnaire de données (musiques, utilisateurs, etc.)
from models import User, Music, Scene, Style, Genre, music_scene, music_style
from App import database
import pafy
from youtube_dl.utils import DownloadError

class DataManager:

    def add_new_user(self, login, password, email):
        user = User()
        user.login = login
        user.email = email
        user.set_passwpord(password)
        database.session.add(user)
        database.session.commit()

    def add_new_musique(self, title, source, loop, style_tags, scene_tags, genre):
        duration = pafy.new(source).length
        music = Music(title=title, source=source, duration=duration, loop=loop, genre=genre, vote=0)
        for style in style_tags:
            music.style_tags.append(Style.query.filter_by(id=style).first())
        for scene in scene_tags:
            music.scene_tags.append(Scene.query.filter_by(id=scene).first())

        try:
            music.sound_url = pafy.new(music.source).getbestaudio().url
            database.session.add(music)
            database.session.commit()
        except OSError as e:
            print(title, "source is unavailable (see:", source, ")")
            print(e)

    def add_music_style_tag(self, name):
        style = Style(name=name)
        database.session.add(style)
        database.session.commit()
    
    def add_music_scene_tag(self, name):
        scene = Scene(name=name)
        database.session.add(scene)
        database.session.commit()

    def add_music_genre(self, name):
        genre = Genre(name=name)
        database.session.add(genre)
        database.session.commit()

    def get_all_musics(self):
        musics = []
        for music in Music.query.order_by(Music.title).all():
            musics.append(music)
        return musics

    def get_musics(self, title, loop, style_tags, scene_tags, genre):
        musics = []
        if title is None:
            title=""
        first_sorted_musics_query = Music.query.filter(Music.title.contains(title))
        if loop is True:
            first_sorted_musics_query = first_sorted_musics_query.filter(Music.loop is loop)
        if genre is not None:
            first_sorted_musics_query = first_sorted_musics_query.filter(Music.genre is genre)

        first_sorted_musics = first_sorted_musics_query.all()
        
        #TODO: il y a sûrement moyen d'optimiser tout ça (bcp trop de boucles...)
        for music in first_sorted_musics:
            if style_tags and style_tags is not None:
                for tag in music.style_tags:
                    if (tag.id in style_tags) and scene_tags is not None and scene_tags:
                        for tag_sc in music.scene_tags:
                            if (tag_sc.id in scene_tags and music not in musics):
                                musics.append(music)
                    else:
                        self.safe_music_list_adding(music, musics)
            elif scene_tags is not None and scene_tags:
                for tag in music.scene_tags:
                    if (tag.id in scene_tags):
                        musics.append(music)
            else:
                musics.append(music)
        return musics
        
