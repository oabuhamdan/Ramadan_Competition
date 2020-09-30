from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.show_home, name="Home"),
    path('register/', views.register, name="Register"),
    path('login/', views.login, name="Login"),
    path('logout/', views.logout, name="Logout"),
]
