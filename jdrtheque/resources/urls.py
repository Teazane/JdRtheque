from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.ScenarioListView.as_view(), name='scenario-list'),
    path('add/', login_required(views.ScenarioCreateView.as_view()), name='scenario-add'),
    path('search/', views.scenario_search, name='scenario-search'),
]