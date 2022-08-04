from django.shortcuts import render
from django.views.generic.list import ListView
from music.models import Music


class MusicListView(ListView):
    model = Music
    paginate_by = 100  # if pagination is desired