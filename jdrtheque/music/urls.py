from django.urls import path
from . import views

urlpatterns = [
    path('', views.MusicListView.as_view(), name='music-list')
]