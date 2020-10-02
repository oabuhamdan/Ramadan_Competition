from django.shortcuts import render, redirect

from .forms import *


# Create your views here.
def show_home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})


def login(request):
    pass


def logout(request):
    pass
