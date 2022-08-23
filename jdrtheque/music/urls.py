from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.MusicListView.as_view(), name='music-list'),
    path('add/', login_required(views.MusicCreateView.as_view()), name='music-add'),
    path("search/", views.music_search, name='music-search'),
    path('scene/add/', login_required(views.SceneCreateView.as_view()), name='scene-add'),
    path('style/add/', login_required(views.StyleCreateView.as_view()), name='style-add'),
    path('genre/add/', login_required(views.GenreCreateView.as_view()), name='genre-add'),
]