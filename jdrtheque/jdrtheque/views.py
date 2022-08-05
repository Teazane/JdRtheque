from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import  render, redirect
from jdrtheque.forms import NewUserForm

class HomePageView(TemplateView):
    template_name = "home.html"


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"form":form})
