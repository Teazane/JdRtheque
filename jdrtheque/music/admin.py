from django.contrib import admin
from music.models import Music, Style, Scene, Genre


class MusicAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'duration', 
        'loop', 
        'vote', 
        'added_by_user', 
    )
    list_filter = ('loop', 'genres', 'styles', 'scenes')
    search_fields = ['title',]

admin.site.register(Music, MusicAdmin)
admin.site.register(Style)
admin.site.register(Scene)
admin.site.register(Genre)
