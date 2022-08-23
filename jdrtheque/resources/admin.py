from django.contrib import admin
from resources.models import Scenario, System, RolePlayGame


class ScenarioAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'min_player_number',
        'max_player_number',
        'duration',
        'vote',
        'rpg',
        'added_by_user',
        'added_date',
    )
    list_filter = ('duration', 'rpg', 'styles',)
    search_fields = ['title',]


class RolePlayGameAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'vf_editor',
        'original_editor',
        'system',
    )
    list_filter = ('vf_editor', 'original_editor', 'styles', 'system')
    search_fields = ['title',]


admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(RolePlayGame, RolePlayGameAdmin)
admin.site.register(System)
