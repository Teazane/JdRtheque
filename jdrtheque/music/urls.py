from django.urls import path
from . import views

urlpatterns = [
    path('', views.MusicListView.as_view(), name='music-list'),
    path('scene/add/', views.SceneCreateView.as_view(), name='scene-add'),
    path('style/add/', views.StyleCreateView.as_view(), name='style-add'),
]