from App import database


music_style = database.Table('music_style',
                             database.Column('style_id', database.Integer, database.ForeignKey('style.id'), primary_key=True),
                             database.Column('music_id', database.Integer, database.ForeignKey('music.id'), primary_key=True)
                             )


music_scene = database.Table('music_scene',
                             database.Column('scene_id', database.Integer, database.ForeignKey('scene.id'), primary_key=True),
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
    sound_url = database.Column(database.String(250), nullable=False)
    duration = database.Column(database.Integer, nullable=False)
    loop = database.Column(database.Boolean, nullable=False)
    vote = database.Column(database.Integer, nullable=False)
    style_tags = database.relationship('Style', secondary=music_style, backref=database.backref('musics', lazy=True))
    scene_tags = database.relationship('Scene', secondary=music_scene, backref=database.backref('musics', lazy=True))
    genre = database.Column(database.Integer, database.ForeignKey('genre.id'), nullable=False)
    added_by_user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=True)


class Style(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), nullable=False, index=True)


class Scene(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), nullable=False, index=True)


class Genre(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), nullable=False, index=True)


class Playlist(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(32), nullable=False)
    musics = database.relationship('Music', secondary=playlist_music)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
