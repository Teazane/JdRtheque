import urllib
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from resources.models import Scenario
from resources.forms import ScenarioSearchForm


class ScenarioListView(ListView):
    model = Scenario
    paginate_by = 100

    def get_queryset(self):
        """
        The scenario queryset can be filtered if any query string has been added to the URL.
        """
        scenarii = Scenario.objects
        title = self.request.GET.get("title", None)
        if title:
            scenarii = scenarii.filter(title__icontains=title)
        author = self.request.GET.get("author", None)
        if author:
            scenarii = scenarii.filter(author__icontains=author)
        min_player_number = self.request.GET.get("min_player_number", None)
        if min_player_number:
            scenarii = scenarii.filter(min_player_number__gte=int(min_player_number))
        max_player_number = self.request.GET.get("max_player_number", None)
        if max_player_number:
            scenarii = scenarii.filter(max_player_number__lte=int(max_player_number))
        duration = self.request.GET.get("duration", None)
        if duration:
            scenarii = scenarii.filter(duration=duration)
        styles = self.request.GET.get("styles", None)
        if styles:
            scenarii = scenarii.filter(styles__in=[int(x) for x in styles.split("-")])
        rpg = self.request.GET.get("rpg", None)
        if rpg:
            scenarii = scenarii.filter(rpg__in=[int(x) for x in rpg.split("-")])
        return scenarii.order_by('-vote').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ScenarioSearchForm()
        return context


def scenario_search(request):
    """ 
    Function used to construct the classical scenario list URL but with query strings.

    .. seealso::
        https://stackoverflow.com/questions/2778247/how-do-i-construct-a-django-reverse-url-using-query-args/5341769#5341769
    """
    if request.method == "POST":
        form = ScenarioSearchForm(request.POST)
        if form.is_valid():
            search_params = {
                "title": form.cleaned_data['title'],
                "author": form.cleaned_data['author'],
                "min_player_number": form.cleaned_data['min_player_number'],
                "max_player_number": form.cleaned_data['max_player_number'],
                "duration": "-".join(str(x) for x in form.cleaned_data['duration']),
                "styles": "-".join(str(x) for x in list(form.cleaned_data['styles'].values_list('pk', flat=True))),
                "rpg": "-".join(str(x) for x in list(form.cleaned_data['rpg'].values_list('pk', flat=True))),
            }
            url = reverse('resources:scenario-list') + '?' + urllib.parse.urlencode(search_params)
            return redirect(url)
        messages.error(request, "Une erreur est survenue lors de la recherche de scénario.")
    return redirect('resources:scenario-list')


class ScenarioCreateView(CreateView, PermissionRequiredMixin):
    model = Scenario
    permission_required = "resources.add_scenario"
    fields = ['title', 'pdf_file', 'description', 'author', 'min_player_number', 'max_player_number', 'duration', 'styles', 'rpg']
    success_url = reverse_lazy('resources:scenario-list')

    def form_valid(self, form):
        messages.success(self.request, "Ajout réussi !" )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de l'ajout.")
        return super().form_invalid(form)
