from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('details/', views.details),
    path('score/', views.score),
]
