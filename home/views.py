from django.shortcuts import render, redirect

from .forms import *


# Create your views here.
def show_home(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.filter(username=request.user.username).first()
        return render(request, "index.html", {'user': user})
    else:
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


def about(request):
    return render(request, 'about-me.html')
