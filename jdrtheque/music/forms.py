from django import forms
from music.models import Genre, Scene, Style


class MusicSearchForm(forms.Form):
    """ 
    Form used to seach musics corresponding to the chosen filter(s).
    """
    title = forms.CharField(label='Titre de la musique', required=False)
    loop = forms.BooleanField(label='Musique bouclable ?', required=False)
    genres = forms.ModelMultipleChoiceField(label='Genre(s) de musique recherché(s)', queryset=Genre.objects.all(), required=False)
    styles = forms.ModelMultipleChoiceField(label='Style(s) de JdR recherché(s)', queryset=Style.objects.all(), required=False)
    scenes = forms.ModelMultipleChoiceField(label='Style(s) de scène de JdR recherché(s)', queryset=Scene.objects.all(), required=False)
