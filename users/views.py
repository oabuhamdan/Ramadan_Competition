from django.shortcuts import render, redirect

from .helper import *
from .models import CustomUser, PointsType, Point


def details(request):
    if request.user.is_authenticated:
        user = request.user
        points = CustomUser.get_points(user.username)
        data = {'points': points, 'user': user}
        return render(request, "details.html", {'data': data})
    else:
        return render(request, '401.html', status=401)


def save_to_db(request):
    user = CustomUser.objects.filter(username=request.user.username).first()
    items = request.POST.dict()
    total = 0.0
    for key, value in items.items():
        pt = PointsType.objects.filter(form_type=key).first()
        if pt is not None and value == 'on':
            point_type = pt
            points, pt_details = get_points_and_details(items, key)
            total = total + points
            Point.objects.create(user=user, type=point_type, value=points, details=pt_details,
                                 record_date=items['record-date'])
    user.total_points = user.total_points + total


def score(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            points_types = PointsType.objects.all()
            data = {'points_types': points_types, 'user': user}
            return render(request, "score.html", {'data': data})
        else:
            save_to_db(request)
            return redirect('/details')
    else:
        return render(request, '401.html', status=401)
