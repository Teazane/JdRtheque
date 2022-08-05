import urllib
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from music.models import Music, Style, Scene, Genre
from music.forms import MusicSearchForm


class MusicListView(ListView):
    model = Music
    paginate_by = 100

    def get_queryset(self):
        """
        The music queryset can be filtered if any query string has been added to the URL.
        """
        musics = Music.objects
        title = self.request.GET.get("title", None)
        if title:
            musics = musics.filter(title__icontains=title)
        loop = self.request.GET.get("loop", None)
        if loop:
            musics = musics.filter(loop=loop)
        styles = self.request.GET.get("styles", None)
        if styles:
            musics = musics.filter(styles__in=[int(x) for x in styles.split("-")])
        genres = self.request.GET.get("genres", None)
        if genres:
            musics = musics.filter(genres__in=[int(x) for x in genres.split("-")])
        scenes = self.request.GET.get("scenes", None)
        if scenes:
            musics = musics.filter(scenes__in=[int(x) for x in scenes.split("-")])
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
            loop_value = int(form.cleaned_data['loop'])
            if loop_value == 0:
                loop = ''
            elif loop_value == 1:
                loop = True
            elif loop_value == 2:
                loop = False
            else:
                messages.error(request, "Une erreur est survenue lors de la recherche de musique.")
                return redirect('music-list')
            search_params = {
                "title": form.cleaned_data['title'],
                "loop": loop,
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
    success_url = reverse_lazy('music-list')

    def form_valid(self, form):
        messages.success(self.request, "Ajout réussi !" )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de l'ajout.")
        return super().form_invalid(form)


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
