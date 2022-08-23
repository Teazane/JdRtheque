from django import forms
from music.models import Style
from resources.models import System, RolePlayGame, Scenario


class ScenarioSearchForm(forms.Form):
    """ 
    Form used to seach scenarii corresponding to the chosen filter(s).
    """
    title = forms.CharField(label='Titre du scénario', required=False)
    author = forms.CharField(label='Auteur du scénario', required=False)
    min_player_number = forms.IntegerField(label='Nombre de joueurs min.', min_value=1, initial=1)
    max_player_number = forms.IntegerField(label='Nombre de joueurs max.', min_value=1, initial=4)
    duration = forms.MultipleChoiceField(label='Durée(s) souhaitée(s)', choices=Scenario.GameDuration.choices, required=False)
    styles = forms.ModelMultipleChoiceField(label='Style(s) de JdR recherché(s)', queryset=Style.objects.all(), required=False)
    rpg = forms.ModelMultipleChoiceField(label='JdR recherché(s)', queryset=RolePlayGame.objects.all(), required=False)
