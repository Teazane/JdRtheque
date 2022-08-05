from django.db import models
from django.contrib.auth.models import User
import pafy

class Style(models.Model):
    """
    Represents the RPG style (ex: horror, steampunk, ...)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Scene(models.Model):
    """
    Represents the scene style (ex: calm, fight, ...)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Genre(models.Model):
    """
    Represents the music style (ex: rock, electro, ...)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Music(models.Model):
    """
    Represents a music object. 

    :param title: Title of the music (max character length set to 200).
    :param source: YouTube source URL (max character length set to 1000).
    :param sound_url: Pafy retreived URL (max character length set to 1000)
    :param duration: Music duration in seconds.
    :param loop: Can the music be looping-played (default to False)?
    :param vote: Upvotes to evaluate the music popularity (default to 0).
    :param styles: The RPG styles associated to the music (ex: horror, steampunk, ...).
    :param scenes: The scene styles associated to the music (ex: calm, fight, ...).
    :param genres: The music styles associated to the music (ex: rock, electro, ...).
    :param added_by_user: The user who has added the music to the platform (can be None).
    :type title: django.db.models.CharField
    :type source: django.db.models.CharField
    :type sound_url: django.db.models.CharField
    :type duration: django.db.models.IntegerField
    :type loop: django.db.models.BooleanField
    :type vote: django.db.models.IntegerField
    :type styles: django.db.models.ManyToManyField(music.models.Style)
    :type scenes: django.db.models.ManyToManyField(music.models.Scene)
    :type genres: django.db.models.ManyToManyField(music.models.Genre)
    :type added_by_user: django.db.models.ForeignKey(django.contrib.auth.models.User)
    """
    title = models.CharField(max_length=200, db_index=True)
    source = models.CharField(max_length=1000)
    sound_url = models.CharField(max_length=1000)
    duration = models.IntegerField()
    loop = models.BooleanField(default=False)
    vote = models.IntegerField(default=0)
    styles = models.ManyToManyField(Style)
    scenes = models.ManyToManyField(Scene)
    genres = models.ManyToManyField(Genre)
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        pafy_music = pafy.new(self.source)
        self.duration = pafy_music.length
        try:
            self.sound_url = pafy_music.getbestaudio().url
        except OSError as e:
            print(title, "source is unavailable (see:", source, ")")
            print(e)
            return
        else:
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]


class Playlist(models.Model):
    """
    Represent a user's playlist containing chosen musics.

    :param title: CharFields(max character length set to 200)
    :param description: Description of the playlist (max character length set to 1000, can be empty)
    :param musics: The musics included in the playlist.
    :param owner: The user owning the playlist.
    :type title: django.db.models.CharFields
    :type description: django.db.models.CharFields
    :type musics: django.db.models.ManyToManyField(music.models.Music)
    :type owner: django.db.models.ForeignKey(django.contrib.auth.models.User)
    """
    title = models.CharField(max_length=200, db_index=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    musics = models.ManyToManyField(Music)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
