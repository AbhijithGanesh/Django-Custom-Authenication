from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import LoginForm
import requests


Direct_url = "http://localhost:8000"

def Landingpage(request):
    return HttpResponse("Welcome to the landing page!")


@login_required(login_url='/Login')
def Second_Page(request):
    return HttpResponse("You've Logged In.")


class GuestLogin(FormView):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form":form})

    def post(self, request):
        form = LoginForm(data = request.POST)
        if form.is_valid():
            requestObject = requests.post(Direct_url+"/api/login", data = form.cleaned_data).json()
            if requestObject['detail']:
                return HttpResponse("Login was successful")
        else:
            print(form.errors)
