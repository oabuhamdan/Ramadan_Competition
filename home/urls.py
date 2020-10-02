from django.urls import path, include

from . import views
from .forms import UserLoginForm
from django.contrib.auth import views as v

urlpatterns = [
    path("", views.show_home, name="Home"),
    path('register/', views.register, name="Register"),
    path('login/',
         v.LoginView.as_view(template_name="registration/login.html", authentication_form=UserLoginForm),
         name='login'),
    path('', include("django.contrib.auth.urls")),

]
