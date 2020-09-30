from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from users.models import *


# Create your views here.
def show_home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User(name=data['name'], username=data['username'], password=data['password'])
            user.save()
            return HttpResponseRedirect('/login')
        else:
            form.add_error('', 'Token hasn\'t been verified, please try again')
            return render(request, 'registrationPage.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registrationPage.html', {'form': form})


def login(request):
    pass


def logout(request):
    pass
