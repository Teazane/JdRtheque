from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from music.models import Music, Style, Scene


class MusicListView(ListView):
    model = Music
    paginate_by = 100  # if pagination is desired


class StyleCreateView(CreateView):
    model = Style
    fields = ['name']
    template_name = "music/style_scene_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_for"] = "style"
        return context


class SceneCreateView(CreateView):
    model = Scene
    fields = ['name']
    template_name = "music/style_scene_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_for"] = "scène"
        return context
