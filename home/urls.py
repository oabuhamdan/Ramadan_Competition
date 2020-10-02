from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.show_home, name="Home"),
    path('register/', views.register, name="Register"),
    path('', include("django.contrib.auth.urls")),
]
