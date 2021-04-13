from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .helper import *
from .models import CustomUser, PointsType, Group


def details(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.filter(username=request.user.username).first()
        is_group_admin = Group.objects.filter(admin=user).first() is not None
        points, total_daily = CustomUser.get_points(user.username)
        data = {'points': points, 'user': user, 'total_daily': total_daily, 'is_group_admin': is_group_admin}
        return render(request, "details.html", {'data': data})
    else:
        return render(request, '401.html', status=401)


def score(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            competition = CustomUser.objects.filter(username=user.username).first().competition
            points_types = PointsType.objects.filter(competition=competition).order_by('section__priority',
                                                                                       '-form_type', 'id')
            data = {'points_types': points_types, 'user': user, 'range': range(1, 31)}
            return render(request, "score.html", {'data': data})
        else:
            save_to_db(request)
            return redirect('/details')
    else:
        return render(request, '401.html', status=401)


def get_requested_user_info(request):
    username = request.GET.get('username')
    points, total_daily = CustomUser.get_points(username)
    data = []
    for point in points.items():
        data.append(
            {
                'day': point[0],
                'point': serializers.serialize('json', point[1]),
                'total': total_daily[point[0]]
            }
        )
    return JsonResponse(data, safe=False)


def fellows_details(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.user.is_authenticated:
        if is_ajax:
            return get_requested_user_info(request)
        else:
            user = CustomUser.objects.filter(username=request.user.username).first()
            group_admin = Group.objects.filter(admin=user).first()
            if group_admin is not None:
                return render(request, "fellows_details.html", {'fellows': group_admin.fellows.all()})
            else:
                return render(request, '401.html', status=401)
    else:
        return render(request, '401.html', status=401)


def standings(request):
    if request.user.is_authenticated:
        user = request.user
        competition = CustomUser.objects.filter(username=user.username).first().competition
        if not competition.show_standings:
            return render(request, '401.html', status=401)
        top_ten_users = CustomUser.objects.filter(competition=competition, total_points__gte=1) \
                            .order_by('-total_points')[:10]
        data = {'top_ten': top_ten_users, 'competition': competition}
        return render(request, "standings.html", {'data': data})
    else:
        return render(request, '401.html', status=401)
