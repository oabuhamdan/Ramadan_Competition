from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .helper import *
from .models import *


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
                'details': ['{} نقاط من {}'.format(int(i.value), i.type.label) for i in point[1]],
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
                users = group_admin.fellows.all()
                group_sum = sum([i.total_points for i in users])
                return render(request, "fellows_details.html",
                              {'fellows': group_admin.fellows.all(), 'group_avg': group_sum / len(users)})
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
                            .order_by('-total_points')[:20]
        data = {'top_ten': top_ten_users, 'competition': competition}
        return render(request, "standings.html", {'data': data})
    else:
        return render(request, '401.html', status=401)


def delete_points(request):
    if request.user.is_staff:
        if request.method == 'GET':
            competitions = Competition.objects.all()
            return render(request, 'delete_points.html', {'competitions': competitions})
        elif request.method == 'POST':
            delete_selected_points(request)
    else:
        return render(request, '401.html', status=401)


def get_competition_people(request):
    if request.user.is_staff:
        selected_competition = request.GET.get('selected_comp')
        comp_people = CustomUser.objects.filter(competition_id=selected_competition)
        data = []
        for person in comp_people:
            data.append(
                {
                    'username': person.username,
                    'name': person.first_name
                }
            )
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse(status=401)


def get_user_points(request):
    if request.user.is_staff:
        selected_user_name = request.GET.get('selected_user')
        selected_day = request.GET.get('selected_day')
        user_points = Point.objects.filter(user__username=selected_user_name, record_date=selected_day)
        data = []
        for point in user_points:
            data.append(
                {
                    'id': point.id,
                    'label': point.type.label,
                    'details': point.details,
                    'value': point.value,
                }
            )
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse(status=401)


def delete_selected_points(request):
    if request.user.is_staff:
        ids = [int(token) for token in request.POST.dict().keys() if token.isdigit()]
        for id in ids:
            Point.objects.filter(id=id).delete()
    return render(request, "delete_points.html")
