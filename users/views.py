from django.contrib import messages
from django.contrib.auth import user_logged_in
from django.http import HttpResponse
from django.shortcuts import render

from .models import CustomUser


def details(request):
    if request.user.is_authenticated:
        user = request.user
        points = CustomUser.get_points(user)
        data = {'points': points, 'user': user}
        return render(request, "details.html", {'data': data})
    else:
        return HttpResponse('Unauthorized', status=401)
    # user = get_object_or_404(CustomUser)
