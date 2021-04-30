from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('details/', views.details),
    path('score/', views.score),
    path('fellows_details/', views.fellows_details),
    path('standings/', views.standings),
    path('delete_points/', views.delete_points),
    path('get_competition_people/', views.get_competition_people),
    path('get_user_points/', views.get_user_points),
]
