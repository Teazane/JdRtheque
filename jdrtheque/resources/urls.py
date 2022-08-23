from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'resources'
urlpatterns = [
    path('scenario/', views.ScenarioListView.as_view(), name='scenario-list'),
    path('scenario/add/', login_required(views.ScenarioCreateView.as_view()), name='scenario-add'),
    path('scenario/search/', views.scenario_search, name='scenario-search'),
]