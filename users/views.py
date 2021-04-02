from django.db.models import QuerySet
from django.template.defaulttags import register
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
            points_types = PointsType.objects.order_by('id', 'section')
            data = {'points_types': points_types, 'user': user}
            return render(request, "score.html", {'data': data})
        else:
            save_to_db(request)
            return redirect('/details')
    else:
        return render(request, '401.html', status=401)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_arabic_section_name(key):
    return arabic_section_names.get(key)
