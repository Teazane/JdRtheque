from django.db import models
from django.core.validators import MinValueValidator 
from django.contrib.auth.models import User
from music.models import Style # Style table should be moved here


class System(models.Model):
    """
    Represents a RPG system.

    :param name: Name of the RPG system (ex: Year Zero Engine, Ubiquity, ...) (max character length set to 200).
    :type name: django.db.models.CharField
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class RolePlayGame(models.Model):
    """
    Represents a role-play game (RPG) object.

    :param title: Title of the RPG (max character length set to 200).
    :param description: Short description of the RPG (max character length set to 1000).
    :param styles: The RPG styles associated (ex: horror, steampunk, ...).
    :param vf_editor: The RPG french editor (max character length set to 200, can be None).
    :param original_editor: The RPG original editor (max character length set to 200). Can't be None so should contain at least "fanmade".
    :param system: The used system to play.
    :type title: django.db.models.CharField
    :type description: django.db.models.CharField
    :type styles: django.db.models.ManyToManyField(music.models.Style)
    :type vf_editor: django.db.models.CharField
    :type original_editor: django.db.models.CharField
    :type system: django.db.models.ForeignKey(resources.models.System)
    """
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    styles = models.ManyToManyField(Style)
    vf_editor = models.CharField(max_length=200, blank=True, null=True)
    original_editor = models.CharField(max_length=200)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Scenario(models.Model):
    """
    Represents a scenario object. 

    :param title: Title of the scenario (max character length set to 200).
    :param pdf_file: A PDF file containing the actual scenario. 
    :param description: Short description of the scenario (max character length set to 1000).
    :param author: The scenario's author (max character length set to 50).
    :param min_player_number: Minimum number of players so that the scenario can be played.
    :param max_player_number: Maximum number of players so that the scenario can be played.
    :param duration: Scenario duration (choice between: "One shot", "Mini-campaign" and "Campaign", default to "One shot").
    :param vote: Upvotes to evaluate the scenario popularity (default to 0).
    :param styles: The RPG styles associated to the scenario (ex: horror, steampunk, ...).
    :param rpg: The RPG used to play the scenario (can be None).
    :param added_by_user: The user who has added the scenario to the platform (can be None).
    :param added_date: Date when the scenario has been added to the DB.
    :type title: django.db.models.CharField
    :type pdf_file: django.bd.models.FileField
    :type description: django.db.models.CharField
    :type author: django.db.models.CharField
    :type min_player_number: django.db.models.IntegerField
    :type max_player_number: django.db.models.IntegerField
    :type source: django.db.models.CharField
    :type sound_url: django.db.models.CharField
    :type duration: django.db.models.IntegerField
    :type loop: django.db.models.BooleanField
    :type vote: django.db.models.IntegerField
    :type styles: django.db.models.ManyToManyField(music.models.Style)
    :type rpg: django.db.models.ForeignKey(resources.models.RolePlayGame)
    :type added_by_user: django.db.models.ForeignKey(django.contrib.auth.models.User)
    :type added_date: django.db.models.DateTimeField
    """
    class GameDuration(models.IntegerChoices):
        """
        Represents a game duration.
        """
        ONE_SHOT = 0, 'One shot'
        MINI_CAMPAIGN = 1, 'Mini-campaign'
        CAMPAIGN = 2, 'Campaign'

    title = models.CharField(max_length=200, db_index=True)
    pdf_file = models.FileField(upload_to='scenarii/')
    description = models.CharField(max_length=1000)
    author = models.CharField(max_length=50)
    min_player_number = models.IntegerField(default=1, validators=[MinValueValidator(1)])  
    max_player_number = models.IntegerField(default=4, validators=[MinValueValidator(1)])  
    duration = models.IntegerField(choices=GameDuration.choices, default=GameDuration.ONE_SHOT)
    vote = models.IntegerField(default=0)
    styles = models.ManyToManyField(Style)
    rpg = models.ForeignKey(RolePlayGame, on_delete=models.SET_NULL, blank=True, null=True)
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
