import urllib
from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from music.models import Music, Style, Scene, Genre
from music.forms import MusicSearchForm


class MusicListView(ListView):
    model = Music
    paginate_by = 100

    def get_queryset(self, **kwargs):
        musics = Music.objects
        title = kwargs.get("title", None)
        if title:
            musics.filter(title__icontains=title)
        loop = kwargs.get("loop", None)
        if loop:
            musics.filter(loop=loop)
        styles = kwargs.get("styles", None)
        if styles:
            musics.filter(styles__in=[int(x) for x in styles.split("-")])
        genres = kwargs.get("genres", None)
        if genres:
            musics.filter(genres__in=[int(x) for x in genres.split("-")])
        scenes = kwargs.get("scenes", None)
        if scenes:
            musics.filter(scenes__in=[int(x) for x in scenes.split("-")])
        return musics.order_by('-vote').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MusicSearchForm()
        return context


def music_search(request):
    """ 
    Function used to construct the classical music list URL but with query strings.

    .. seealso::
        https://stackoverflow.com/questions/2778247/how-do-i-construct-a-django-reverse-url-using-query-args/5341769#5341769
    """
    if request.method == "POST":
        form = MusicSearchForm(request.POST)
        if form.is_valid():
            search_params = {
                "title": form.cleaned_data['title'],
                "loop": form.cleaned_data['loop'],
                "styles": "-".join(str(x) for x in list(form.cleaned_data['styles'].values_list('pk', flat=True))),
                "genres": "-".join(str(x) for x in list(form.cleaned_data['genres'].values_list('pk', flat=True))),
                "scenes": "-".join(str(x) for x in list(form.cleaned_data['scenes'].values_list('pk', flat=True))),
            }
            url = reverse('music-list') + '?' + urllib.parse.urlencode(search_params)
            return redirect(url)
        messages.error(request, "Une erreur est survenue lors de la recherche de musique.")
    return redirect('music-list')


class MusicCreateView(CreateView, PermissionRequiredMixin):
    model = Music
    permission_required = "music.add_music"
    fields = ['title', 'source', 'loop', 'styles', 'scenes', 'genres']


class StyleCreateView(CreateView, PermissionRequiredMixin):
    model = Style
    permission_required = "music.add_style"
    fields = ['name']
    template_name = "music/style_scene_genre_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_for"] = "style"
        return context


class SceneCreateView(CreateView, PermissionRequiredMixin):
    model = Scene
    permission_required = "music.add_scene"
    fields = ['name']
    template_name = "music/style_scene_genre_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_for"] = "scène"
        return context


class GenreCreateView(CreateView, PermissionRequiredMixin):
    model = Genre
    permission_required = "music.add_genre"
    fields = ['name']
    template_name = "music/style_scene_genre_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_for"] = "genre"
        return context
