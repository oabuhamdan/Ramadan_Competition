from django.contrib import admin
from django.urls import path, include

from admins import views

urlpatterns = [
    path('delete_selected_points/', views.delete_selected_points),
    path('delete_points/', views.delete_points),
    path('get_competition_people/', views.get_competition_people),
    path('get_user_points/', views.get_user_points),
    path('', views.admin_home),
]
