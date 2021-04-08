from django.shortcuts import render, redirect

from .helper import *
from .models import CustomUser, PointsType, Point


def details(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.filter(username=request.user.username).first()
        points, total_daily = CustomUser.get_points(user.username)
        data = {'points': points, 'user': user, 'total_daily': total_daily}
        return render(request, "details.html", {'data': data})
    else:
        return render(request, '401.html', status=401)


def score(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            competition = CustomUser.objects.filter(username=user.username).first().competition
            points_types = PointsType.objects.filter(competition=competition).order_by('id', 'section')
            data = {'points_types': points_types, 'user': user, 'range': range(1, 31)}
            return render(request, "score.html", {'data': data})
        else:
            save_to_db(request)
            return redirect('/details')
    else:
        return render(request, '401.html', status=401)
