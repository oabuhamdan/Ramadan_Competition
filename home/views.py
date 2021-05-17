from django.shortcuts import render, redirect

from users.helper import get_ramadan_daily_message
from .forms import *


# Create your views here.
def show_home(request):
    data = {'ramadan_daily_message': get_ramadan_daily_message(), }
    if request.user.is_authenticated:
        user = CustomUser.objects.filter(username=request.user.username).first()
        request.session['competition_archive_mode'] = user.competition.archive_mode
        data['user'] = user
        return render(request, "index.html", data)
    else:
        return render(request, "index.html", data)


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


def about(request):
    return render(request, 'about-team.html')


def about_me(request):
    return render(request, 'about-me.html')
