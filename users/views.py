from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.
def show_user_page(request, username):
    user = get_object_or_404(User, username=username)
