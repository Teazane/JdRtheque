from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from music.models import Music, Style, Scene, Genre


class MusicListView(ListView):
    model = Music
    paginate_by = 100


class MusicCreateView(CreateView, PermissionRequiredMixin):
    model = Music
    permission_required = "music.add_music"
    fields = [
        'title',
        'source',
        'loop',
        'styles',
        'scenes',
        'genres',
    ]


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
