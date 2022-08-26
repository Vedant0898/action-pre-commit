from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegisterUserForm
# Create your views here.


def register(request):

    if request.method != "POST":
        #display blank form
        form = RegisterUserForm()
    
    else:
        #POST data submitted
        form = RegisterUserForm(data = request.POST)

        if form.is_valid():
            form.save()

            authenticated_user = authenticate(username = request.POST['username'],password = request.POST['password1'])
            login(request,authenticated_user)

            return HttpResponseRedirect(reverse("Sports:index"))
    
    context = {"form":form}

    return render(request,"Users/register.html",context=context)


def login_user(request):

    if request.method !="POST":
        #display a blank form
        form = AuthenticationForm(request)
    
    else:
        form = AuthenticationForm(request,data = request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return HttpResponseRedirect(reverse("Sports:index"))

    context = {"form":form}

    return render(request,"Users/login.html",context=context)



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("Sports:index"))
