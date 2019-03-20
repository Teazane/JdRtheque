# Gestionnaire de données (musiques, utilisateurs, etc.)
from models import User, Music, Scene, Style, music_scene, music_style
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

    def add_new_musique(self, title, source, loop, style_tags, scene_tags):
        duration = pafy.new(source).length
        music = Music(title=title, source=source, duration=duration, loop=loop, vote=0)
        for style in style_tags:
            music.style_tags.append(Style.query.filter_by(id=style).first())
        for scene in scene_tags:
            music.scene_tags.append(Scene.query.filter_by(id=scene).first())

        database.session.add(music)
        database.session.commit()

    def add_music_style_tag(self, name):
        style = Style(name=name)
        database.session.add(style)
        database.session.commit()
    
    def add_music_scene_tag(self, name):
        scene = Scene(name=name)
        database.session.add(scene)
        database.session.commit()

    def safe_music_list_adding(self, music, music_list):
        try:
            music_url_stream = pafy.new(music.source).getbestaudio().url
            music_list.append((music,music_url_stream))
        except OSError as e:
            print(music.title, "source is unavailable (see:", music.source, ")")
            print(e)
            music_list.append((music,""))

    def get_all_musics(self):
        musics = []
        for music in Music.query.order_by(Music.title).all():
            self.safe_music_list_adding(music, musics)
        return musics

    def get_musics(self, title, loop, style_tags, scene_tags):
        musics = []
        if title is None:
            title=""
        if loop is False:
            first_sorted_musics = Music.query.filter(Music.title.contains(title)).all()
        else :
            first_sorted_musics = Music.query.filter(Music.title.contains(title)).filter(Music.loop is loop).all()
        
        #TODO: il y a sûrement moyen d'optimiser tout ça (bcp trop de boucles...)
        for music in first_sorted_musics:
            if style_tags and style_tags is not None:
                for tag in music.style_tags:
                    if (tag.id in style_tags) and scene_tags is not None and scene_tags:
                        for tag_sc in music.scene_tags:
                            if (tag_sc.id in scene_tags and music not in musics):
                                self.safe_music_list_adding(music, musics)
                    else:
                        self.safe_music_list_adding(music, musics)
            elif scene_tags is not None and scene_tags:
                for tag in music.scene_tags:
                    if (tag.id in scene_tags):
                        self.safe_music_list_adding(music, musics)
            else:
                self.safe_music_list_adding(music, musics)
        return musics
        
