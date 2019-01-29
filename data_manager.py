# Gestionnaire de données (musiques, utilisateurs, etc.)
from models import User, Music, Scene, Style, music_scene, music_style
from App import database


class DataManager:

    def add_new_user(self, login, password, email):
        user = User()
        user.login = login
        user.email = email
        user.set_passwpord(password)
        database.session.add(user)
        database.session.commit()

    def add_new_musique(self, title, source, duration, loop, style_tags, scene_tags):
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

    def get_all_musics(self):
        musics = []
        for music in Music.query.order_by(Music.title).all():
            musics.append(music)
        return musics

    def get_musics(self, title, loop, style_tags, scene_tags):
        musics = []
        if title is None:
            title=""
        if loop is False:
            print("On fait le tri par titre")
            first_sorted_musics = Music.query.filter(Music.title.contains(title)).all()
            print(first_sorted_musics)
        else :
            print("On fait le tri par titre et loop")
            first_sorted_musics = Music.query.filter(Music.title.contains(title)).filter(Music.loop is loop).all()
            print(first_sorted_musics)
        
        #TODO: il y a sûrement moyen d'optimiser tout ça (bcp trop de boucles...)
        for music in first_sorted_musics:
            if style_tags and style_tags is not None:
                for tag in music.style_tags:
                    if (tag.id in style_tags):
                        if scene_tags is not None and scene_tags:
                            for tag_sc in music.scene_tags:
                                if (tag_sc.id in scene_tags and music not in musics):
                                    musics.append(music)
                        else:
                            musics.append(music)
            elif scene_tags is not None and scene_tags:
                for tag in music.scene_tags:
                    if (tag.id in scene_tags):
                        musics.append(music)
            else:
                musics.append(music)
        
        return musics
        
